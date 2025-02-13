import asyncio
import random
from pyrogram import Client, filters
from pyrogram.errors import FloodWait, UsernameOccupied

# 🔥 Bot Configuration
api_id = 20855254
api_hash = "deffab389ffe1fe418beab319de55115"
session_string = "BQE-OdYAVbCjcYHfx68jv2AKkxKuBpSDxQGi_inap6ti77uInRNGdU7SxMLbkF4fhWsjqwWQX5_MQviALU2zN5PktfP21KdXUFHSyXsxYPgu0y2gxxI5eVJ03RK5guJKcEUO6soXovGAr09pgV6vEDfvrJWQ98s9Z_MtbG0utuMAaaC8QNOd_muxJ0LeNMmqTOph_Z_023gjxFvWY6FhafFDOXNWUtwv5h0My80xgoydA93EWiyHAZ5lV1HKKnWse8-ZdQASJNSpD7mLiWGk1JEgOxp7iuT7NqthGNhLm9i4_EQb6ccFwz4bmrJKeR30cjO4GpImkfOwu8ZQq7Wf8vyX6SC_IQAAAAF-vnXaAA"

# ✅ Default Configs
invite_link = "https://t.me/+ctEPhH39dL4yYzJl"  # Permanent Private Link
channel_username = "thechatterhood"  # Channel username (without @)
log_channel_id = -1002361577280  # Log Channel ID (Yahan history jayegi)
message_id = 3  # Channel pe jo existing message hai uska ID
default_interval = 1800  # Default Interval (30 min)
intervals_dict = {}  # Har group ka custom interval store karega

app = Client("owner_session", api_id=api_id, api_hash=api_hash, session_string=session_string)

def generate_username():
    """🔥 Random username generate karega with 'chatterhood'"""
    return f"chatterhood_{random.randint(1000, 9999)}"

async def change_username(chat_id=None, force=False):
    """🔥 Group ka username change karega (Force ya Scheduled)"""
    async with app:
        while True:
            if not force:  # Agar forcechange nahi hai toh interval ka wait karega
                interval = intervals_dict.get(chat_id, default_interval)
                await asyncio.sleep(interval)

            try:
                # ✅ Group ID dynamically fetch karo
                chat = await app.get_chat(invite_link)
                group_id = chat.id  
                print(f"✅ Group found: {chat.title} ({group_id})")

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

                    # ✅ Log Channel me username history bhejo
                    await app.send_message(log_channel_id, f"🔹 **New Username Set:** @{new_username}")

                except Exception as e:
                    print(f"🚨 Message edit error: {e}")

                if force:  # Agar forcechange hai toh loop break kar do
                    break

            except Exception as e:
                print(f"🚨 Could not fetch group via invite link: {e}")
                await asyncio.sleep(30)

# 🎛 /setinterval Command (Admins Only)
@app.on_message(filters.command("setinterval") & filters.group)
async def set_interval(client, message):
    if not message.from_user:
        return

    user_id = message.from_user.id
    chat_id = message.chat.id

    # ✅ Only admins can set interval
    member = await client.get_chat_member(chat_id, user_id)
    if not (member.status in ["administrator", "owner"]):
        return await message.reply_text("❌ **Only admins can set interval!**")

    try:
        seconds = int(message.command[1])
        if seconds < 60 or seconds > 86400:
            return await message.reply_text("❌ Interval must be between 1 minute (60s) and 24 hours (86400s)!")

        intervals_dict[chat_id] = seconds
        await message.reply_text(f"✅ **Interval set to {seconds} seconds!**")

    except (IndexError, ValueError):
        await message.reply_text("❌ Usage: `/setinterval <seconds>` (60s to 86400s)")

# ⚡ /forcechange Command (Admins Only)
@app.on_message(filters.command("forcechange") & filters.group)
async def force_change(client, message):
    if not message.from_user:
        return

    user_id = message.from_user.id
    chat_id = message.chat.id

    # ✅ Only admins can force change
    member = await client.get_chat_member(chat_id, user_id)
    if not (member.status in ["administrator", "owner"]):
        return await message.reply_text("❌ **Only admins can force change username!**")

    await message.reply_text("🔄 **Forcing username change...**")
    await change_username(chat_id, force=True)  # Instant change call

# 🚀 Run Bot
print("✅ Bot is running...")
app.run(change_username())
