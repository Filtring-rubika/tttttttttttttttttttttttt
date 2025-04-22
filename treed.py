import telebot
import requests
import threading
import time

# توکن ربات
TOKEN = '7604187497:AAFajdGaG9OTOz7hEhcCpwp2Um2YsXgaUVM'
bot = telebot.TeleBot(TOKEN)

# چت آی‌دی برای ارسال هشدار (در حالت تست دستی وارد کنید)
chat_id = 'CHAT_ID_اینجا'

# لیست آلارم قیمت‌ها (ارز: قیمت هدف)
alarms = {
    "btc": 26000,
    "eth": 1800
}

# تابع دریافت قیمت ارز دیجیتال (مثال با BTC و ETH)
def get_price(symbol):
    try:
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={symbol}&vs_currencies=usd"
        response = requests.get(url)
        data = response.json()
        return data[symbol]["usd"]
    except Exception as e:
        return None

# چک کردن هشدار قیمت‌ها
def check_alarms():
    while True:
        for symbol, target in alarms.items():
            price = get_price(symbol)
            if price and price >= target:
                bot.send_message(chat_id, f"هشدار! قیمت {symbol.upper()} رسید به {price}$")
        time.sleep(60)

# دستور /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    global chat_id
    chat_id = message.chat.id
    bot.reply_to(message, "سلام! ربات آماده‌ی تحلیل و هشدار قیمتیه.")

# دستور /help
@bot.message_handler(commands=['help'])
def help_command(message):
    bot.reply_to(message, "نام ارز رو بفرست مثل BTC یا ETH تا تحلیل دریافت کنی.")

# تحلیل ساده ارز
@bot.message_handler(func=lambda m: True)
def handle_message(message):
    text = message.text.lower()
    if text in ['btc', 'eth']:
        price = get_price(text)
        if price:
            trend = "صعودی" if price > alarms[text] else "خنثی یا نزولی"
            bot.reply_to(message, f"قیمت فعلی {text.upper()}: {price}$ - تحلیل: {trend}")
        else:
            bot.reply_to(message, "دریافت قیمت ممکن نیست. بعداً امتحان کن.")
    else:
        bot.reply_to(message, f"دستور نامعتبر. فقط نام ارز رو وارد کن.")

# اجرای ترد آلارم و شروع ربات
def run_bot():
    alarm_thread = threading.Thread(target=check_alarms)
    alarm_thread.daemon = True
    alarm_thread.start()
    print("ربات اجرا شد...")
    bot.polling()

if __name__ == "__main__":
    run_bot()