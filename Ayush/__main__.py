import os
import logging
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import ChatAdminRequired, PeerIdInvalid
from pyrogram.enums import ChatMembersFilter

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

# Config vars (Render / Termux me ENV set karna hoga)
API_ID = int(os.getenv("API_ID", 0))
API_HASH = os.getenv("API_HASH", "")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
OWNER = os.getenv("OWNER", "")

# Bot client
app = Client(
    "banall",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
)

# /start command
@app.on_message(filters.command("start") & filters.private)
async def start_command(client, message: Message):
    await message.reply_photo(
        photo="https://telegra.ph/file/b26847056f19c1b5d7712.jpg",
        caption=(
            "🥀 ʜᴇʏ! ɪ ᴀᴍ **ʙᴀɴᴀʟʟ ʙᴏᴛ** 🤖🔥\n\n"
            "⚠️ Nᴏᴛᴇ: Usᴇ Tʜɪs Bᴏᴛ Fᴏʀ Fᴜɴ & Gʀᴏᴜᴘ Mᴀɴᴀɢᴇᴍᴇɴᴛ!"
        ),
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("👑 ᴏᴡɴᴇʀ", url=f"https://t.me/{OWNER}")]]
        )
    )

# /banall command
@app.on_message(filters.command("banall") & filters.group)
async def banall_command(client, message: Message):
    if not message.from_user:
        return
    
    # Check admin
    admins = [
        admin.user.id async for admin in client.get_chat_members(
            message.chat.id, filter=ChatMembersFilter.ADMINISTRATORS
        )
    ]
    if message.from_user.id not in admins:
        await message.reply("❌ Only admins can use this command!")
        return

    await message.reply("⚡ Sᴛᴀʀᴛɪɴɢ Bᴀɴᴀʟʟ Pʀᴏᴄᴇss...")

    async for member in client.get_chat_members(message.chat.id):
        try:
            if member.user.is_bot or member.user.id in admins:
                continue
            await client.ban_chat_member(chat_id=message.chat.id, user_id=member.user.id)
            logging.info(f"Banned {member.user.id} from {message.chat.id}")
        except ChatAdminRequired:
            await message.reply("⚠️ I need **Ban Members** permission!")
            break
        except PeerIdInvalid:
            continue
        except Exception as e:
            logging.warning(f"Failed to ban {member.user.id}: {e}")

    await message.reply("✅ Bᴀɴᴀʟʟ Pʀᴏᴄᴇss Cᴏᴍᴘʟᴇᴛᴇᴅ!")

# Run bot
if __name__ == "__main__":
    print("🚀 Banall Bot Booted Successfully")
    app.run()
