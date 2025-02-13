import asyncio
import random
from pyrogram import Client
from pyrogram.errors import FloodWait, UsernameOccupied

api_id = 20855254  # Apna API ID
api_hash = "deffab389ffe1fe418beab319de55115"
session_string = "your_session_string_here"  # Owner account ka session

group_id = -1002340048520   # Group ka chat ID
channel_id = -1002467130777  # Channel ID jisme update jayega
message_id = 3  # Channel pe jo existing message hai uska ID
interval = 1800  # Kitne seconds ke baad change ho (e.g., 3600 = 1 hour)

app = Client("owner_session", api_id=api_id, api_hash=api_hash, session_string=session_string)

def generate_username():
    words = ["alpha", "beta", "gamma", "delta", "sigma", "omega"]
    return f"{random.choice(words)}_{random.randint(1000, 9999)}"

async def change_username():
    async with app:
        while True:
            while True:
                new_username = generate_username()
                try:
                    await app.set_chat_username(group_id, new_username)
                    print(f"Username changed to @{new_username}")
                    break
                except UsernameOccupied:
                    print(f"Username @{new_username} already taken, trying again...")
                    await asyncio.sleep(2)
                except FloodWait as e:
                    print(f"Rate limit! Waiting {e.value} seconds...")
                    await asyncio.sleep(e.value)
                except Exception as e:
                    print(f"Error: {e}")
                    return

            try:
                await app.edit_message_text(channel_id, message_id, f"@{new_username}")
                print("Channel message updated.")
            except Exception as e:
                print(f"Message edit error: {e}")

            try:
                await app.revoke_chat_invite_link(group_id)
                print("Private invite link revoked.")
            except Exception as e:
                print(f"Invite revoke error: {e}")

            await asyncio.sleep(interval)

app.run(change_username())
