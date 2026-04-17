from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ChatMemberHandler,
    ContextTypes,
    filters,
)

import time

BOT_TOKEN = ""

# user_id -> {expiry, chat_id}
pending_users = {}
verified_users = set()

async def debug_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.effective_message

    print("========== DEBUG MESSAGE ==========")
    print("CHAT ID:", update.effective_chat.id)
    print("THREAD ID:", msg.message_thread_id)
    print("TEXT:", msg.text)


# =========================
# JOIN HANDLER (NEW CHAT MEMBERS)
# =========================
async def handle_join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message

    if not message or not message.new_chat_members:
        return

    chat_id = update.effective_chat.id

    for user in message.new_chat_members:
        print("🟢 JOIN DETECTED:", user.id, user.first_name)

        pending_users[user.id] = {
            "expiry": time.time() + 60,
            "chat_id": chat_id
        }

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("✅ Verifikasi", callback_data=f"verify_{user.id}")]
        ])

        # await context.bot.send_message(
        #     chat_id=chat_id,
        #     text=f"👋 {user.first_name}, verifikasi dalam 1 menit!",
        #     reply_markup=keyboard
        # )
        await context.bot.send_message(
            chat_id=chat_id,
            message_thread_id=23,
            text=f"👋 @{user.username}, verifikasi dalam 1 menit!",
            reply_markup=keyboard
        )

# =========================
# BUTTON VERIFY
# =========================
async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    data = query.data

    if data == f"verify_{user_id}":
        if user_id in pending_users:
            verified_users.add(user_id)
            del pending_users[user_id]

            await query.edit_message_text("✅ Kamu sudah diverifikasi!")
            print("🟢 VERIFIED:", user_id)
        else:
            await query.answer("Sudah expired / sudah verified", show_alert=True)


# =========================
# DELETE MESSAGE IF NOT VERIFIED
# =========================
async def delete_unverified_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return

    user_id = update.message.from_user.id

    if user_id in pending_users and user_id not in verified_users:
        try:
            await update.message.delete()
            print("🗑 DELETE:", user_id)
        except Exception as e:
            print("DELETE ERROR:", e)


# =========================
# TIMEOUT CHECK (KICK)
# =========================
async def check_timeout(context: ContextTypes.DEFAULT_TYPE):
    now = time.time()

    for user_id in list(pending_users.keys()):
        data = pending_users[user_id]

        if now > data["expiry"]:
            chat_id = data["chat_id"]

            try:
                await context.bot.ban_chat_member(chat_id, user_id)
                await context.bot.unban_chat_member(chat_id, user_id)

                del pending_users[user_id]

                await context.bot.send_message(
                    chat_id,
                    f"⛔ User {user_id} tidak verifikasi → dikick"
                )

                print("⛔ KICKED:", user_id)

            except Exception as e:
                print("KICK ERROR:", e)

async def unban(bot):
    await bot.unban_chat_member(-1003987991659, 6668318682)
    print("UNBANNED")


# =========================
# MAIN
# =========================
def main():
    print("🚀 BOT STARTED")

    app = Application.builder().token(BOT_TOKEN).build()

    # run unban AFTER bot ready
    # async def post_init(app):
    #     await unban(app.bot)

    # app.post_init = post_init

    # JOIN HANDLER (INI YANG BENAR UNTUK CASE KAMU)
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, handle_join))

    # BUTTON CALLBACK
    app.add_handler(CallbackQueryHandler(button_click))

    # DELETE MESSAGE
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, delete_unverified_messages))

    # PERIODIC CHECK
    app.job_queue.run_repeating(check_timeout, interval=10, first=10)

    print("✅ HANDLERS LOADED")

    app.run_polling()
    

if __name__ == "__main__":
    main()