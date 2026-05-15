import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from openai import OpenAI
load_dotenv()

# Telegram Bot Token
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# OpenRouter API Key
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# AI Client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)

# Start Command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 AI Reply Assistant is now active!"
    )

# AI Reply Function
async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_message = update.message.text

    try:
        completion = client.chat.completions.create(
            model="openai/gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a professional AI assistant that writes short and smart replies to messages."
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ]
        )

        ai_reply = completion.choices[0].message.content

        await update.message.reply_text(ai_reply)

    except Exception as e:
        print(e)
        await update.message.reply_text(str(e))

# Build App
app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

# Handlers
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))

print("AI Telegram Bot is running...")

# Run Bot
app.run_polling()