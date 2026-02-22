import os
import telebot
import google.generativeai as genai
from flask import Flask
from threading import Thread

# Flask setup for Render (Bot ကို နိုးနေအောင် လုပ်ပေးတာပါ)
app = Flask(__name__)
@app.route('/')
def home(): return "Bot is running!"

# Key တွေကို Render ရဲ့ Environment Variables ထဲမှာ နောက်မှ ထည့်ပါမယ်
BOT_TOKEN = os.environ.get('BOT_TOKEN')
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')

# AI Configuration
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "မင်္ဂလာပါ! ကျွန်တော်က Gemini AI Bot ပါ။ Content တစ်ခုခု ရေးခိုင်းကြည့်ပါဗျ။")

@bot.message_handler(func=lambda message: True)
def ai_reply(message):
    try:
        response = model.generate_content(message.text)
        bot.reply_to(message, response.text)
    except Exception as e:
        print(f"Error: {e}")
        bot.reply_to(message, "Error တစ်ခုခု တက်နေပါတယ်ဗျာ။")

def run_bot():
    bot.infinity_polling()

if __name__ == "__main__":
    # Bot ကို Thread တစ်ခုနဲ့ Run ပြီး Flask ကို တစ်ပြိုင်နက် Run မယ်
    t = Thread(target=run_bot)
    t.start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
