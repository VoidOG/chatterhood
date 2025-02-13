import asyncio
import random
from datetime import datetime
import pytz  # 🔥 Timezone Handling
from pyrogram import Client
from pyrogram.errors import FloodWait, UsernameOccupied

# 🔥 Bot Configuration
api_id = 20855254
api_hash = "deffab389ffe1fe418beab319de55115"
session_string = "BQE-OdYAVbCjcYHfx68jv2AKkxKuBpSDxQGi_inap6ti77uInRNGdU7SxMLbkF4fhWsjqwWQX5_MQviALU2zN5PktfP21KdXUFHSyXsxYPgu0y2gxxI5eVJ03RK5guJKcEUO6soXovGAr09pgV6vEDfvrJWQ98s9Z_MtbG0utuMAaaC8QNOd_muxJ0LeNMmqTOph_Z_023gjxFvWY6FhafFDOXNWUtwv5h0My80xgoydA93EWiyHAZ5lV1HKKnWse8-ZdQASJNSpD7mLiWGk1JEgOxp7iuT7NqthGNhLm9i4_EQb6ccFwz4bmrJKeR30cjO4GpImkfOwu8ZQq7Wf8vyX6SC_IQAAAAF-vnXaAA"  # Owner account ka session

# ✅ Default Configs
invite_link = "https://t.me/+ctEPhH39dL4yYzJl"  # Group Permanent Private Link
channel_username = "thechatterhood"  # Channel username (without @)
log_channel_invite = "https://t.me/+Xlfwauvv51EzOTdl"  # 🔥 Log Channel Invite Link
message_id = 3  # Channel pe jo existing message hai uska ID
interval = 900  # Kitne seconds ke baad change ho (e.g., 30 min)

app = Client("owner_session", api_id=api_id, api_hash=api_hash, session_string=session_string)

# 🔥 IST Timezone Set Karna
IST = pytz.timezone("Asia/Kolkata")

def generate_username():
    """🔥 Random username generate karega with 'chatterhood'"""
    return f"chatterhood_{random.randint(1000, 9999)}"

async def change_username():
    async with app:
        while True:
            try:
                # ✅ Group ID dynamically fetch karo
                chat = await app.get_chat(invite_link)
                group_id = chat.id  
                print(f"✅ Group found: {chat.title} ({group_id})")

                # ✅ Log Channel ID dynamically fetch karo
                log_chat = await app.get_chat(log_channel_invite)
                log_channel_id = log_chat.id  
                print(f"✅ Log Channel found: {log_chat.title} ({log_channel_id})")

                while True:
                    new_username = generate_username()
                    try:
                        await app.set_chat_username(group_id, new_username)
                        print(f"✅ Username changed to @{new_username}")
                        break
                    except UsernameOccupied:
                        print(f"❌ Username @{new_username} already taken, trying again...")
                        await asyncio.sleep(2)
                    except FloodWait as e:
                        print(f"⏳ Rate limit! Waiting {e.value} seconds...")
                        await asyncio.sleep(e.value)
                    except Exception as e:
                        print(f"🚨 Error while changing username: {e}")
                        return

                try:
                    # ✅ Channel ID dynamically fetch karo
                    channel = await app.get_chat(channel_username)
                    channel_id = channel.id  
                    print(f"✅ Channel found: {channel.title} ({channel_id})")

                    # ✅ Message edit karo
                    await app.edit_message_text(channel_id, message_id, f"@{new_username}")
                    print("✅ Channel message updated.")

                    # ✅ Log Channel me username history bhejo (IST Timezone ke saath)
                    timestamp = datetime.now(IST).strftime("%Y-%m-%d %I:%M:%S %p")  # 🔥 IST Format
                    log_message = f"📌 **New Username Set:** @{new_username}\n🕒 **Time:** {timestamp} (IST)"
                    await app.send_message(log_channel_id, log_message)
                    print("✅ Log Channel updated.")

                except Exception as e:
                    print(f"🚨 Message edit error: {e}")

                await asyncio.sleep(interval)

            except Exception as e:
                print(f"🚨 Could not fetch group or log channel via invite link: {e}")
                await asyncio.sleep(30)

app.run(change_username())
