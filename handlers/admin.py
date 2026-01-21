"""
Admin Command Handlers
Handles admin-only commands like /userscount, /broadcast, etc.
"""
import os
import json
from datetime import datetime
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command

import config
from locales import get_text

router = Router()


def is_admin(user_id: int) -> bool:
    """Check if user is an admin"""
    return user_id in config.ADMIN_IDS


async def get_user_settings(user_id: int):
    """Get user language settings"""
    from storage.json_storage import UserDataManager
    user_manager = UserDataManager(user_id)
    await user_manager.load()
    settings = user_manager.data.get("settings", {})
    lang = settings.get("language", "en")
    return lang


@router.message(Command("userscount"))
async def cmd_users_count(message: Message):
    """Show total users count - Admin only"""
    user_id = message.from_user.id
    lang = await get_user_settings(user_id)
    
    if not is_admin(user_id):
        await message.answer(get_text("admin_only", lang))
        return
    
    # Count user files in data/users directory
    users_dir = config.USERS_DIR
    
    if not os.path.exists(users_dir):
        await message.answer("📊 *Admin Panel*\n\n👥 Total users: 0", parse_mode="Markdown")
        return
    
    user_files = [f for f in os.listdir(users_dir) if f.endswith('.json')]
    total_users = len(user_files)
    
    # Get more detailed stats
    active_today = 0
    active_week = 0
    total_words_learned = 0
    
    now = datetime.now()
    
    for user_file in user_files:
        try:
            file_path = os.path.join(users_dir, user_file)
            with open(file_path, 'r', encoding='utf-8') as f:
                user_data = json.load(f)
            
            # Count words learned
            learned_4000 = user_data.get("learned_words_4000", {})
            custom_vocab = user_data.get("custom_vocabulary", [])
            total_words_learned += len(learned_4000) + len(custom_vocab)
            
            # Check last activity
            stats = user_data.get("stats", {})
            last_activity = stats.get("last_activity")
            if last_activity:
                try:
                    last_active = datetime.fromisoformat(last_activity)
                    days_ago = (now - last_active).days
                    if days_ago == 0:
                        active_today += 1
                    if days_ago <= 7:
                        active_week += 1
                except:
                    pass
        except:
            continue
    
    stats_text = f"""📊 *Admin Panel - Statistics*

👥 *Total Users:* {total_users}

📈 *Activity:*
• Active today: {active_today}
• Active this week: {active_week}

📚 *Learning:*
• Total words learned: {total_words_learned}
• Avg words/user: {total_words_learned // total_users if total_users > 0 else 0}
"""
    
    await message.answer(stats_text, parse_mode="Markdown")


@router.message(Command("broadcast"))
async def cmd_broadcast(message: Message):
    """Broadcast message to all users - Admin only"""
    user_id = message.from_user.id
    lang = await get_user_settings(user_id)
    
    if not is_admin(user_id):
        await message.answer(get_text("admin_only", lang))
        return
    
    # Get the message to broadcast (text after /broadcast)
    broadcast_text = message.text.replace("/broadcast", "").strip()
    
    if not broadcast_text:
        await message.answer(
            "📢 *Broadcast Message*\n\n"
            "Usage: `/broadcast Your message here`\n\n"
            "This will send the message to all users.",
            parse_mode="Markdown"
        )
        return
    
    users_dir = config.USERS_DIR
    if not os.path.exists(users_dir):
        await message.answer("No users found.")
        return
    
    user_files = [f for f in os.listdir(users_dir) if f.endswith('.json')]
    
    sent_count = 0
    failed_count = 0
    
    status_msg = await message.answer(f"📤 Broadcasting to {len(user_files)} users...")
    
    for user_file in user_files:
        try:
            target_user_id = int(user_file.replace('.json', ''))
            await message.bot.send_message(
                chat_id=target_user_id,
                text=f"📢 *Announcement*\n\n{broadcast_text}",
                parse_mode="Markdown"
            )
            sent_count += 1
        except Exception as e:
            failed_count += 1
    
    await status_msg.edit_text(
        f"📢 *Broadcast Complete*\n\n"
        f"✅ Sent: {sent_count}\n"
        f"❌ Failed: {failed_count}",
        parse_mode="Markdown"
    )


@router.message(Command("adminhelp"))
async def cmd_admin_help(message: Message):
    """Show admin commands - Admin only"""
    user_id = message.from_user.id
    lang = await get_user_settings(user_id)
    
    if not is_admin(user_id):
        await message.answer(get_text("admin_only", lang))
        return
    
    help_text = """🔧 *Admin Commands*

/userscount - Show user statistics
/broadcast <message> - Send message to all users
/adminhelp - Show this help

*Example:*
`/broadcast Hello everyone! New update available!`
"""
    
    await message.answer(help_text, parse_mode="Markdown")
