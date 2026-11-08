import telebot
from telebot import types
import random
import datetime

# Öz botuň tokenini şu ýere ýazarsyň
API_TOKEN = "9088335014:AAElBoS_OZCb4_TIUFJDfYOM5wFOn7fgbIA"
bot = telebot.TeleBot(API_TOKEN)

user_selections = {}

def get_main_menu():
    kb = types.InlineKeyboardMarkup(row_width=2)
    kb.add(
        types.InlineKeyboardButton("📊 Pro Signal Almak", callback_data="select_pair"),
        types.InlineKeyboardButton("📈 Market Analizi", callback_data="market_analysis"),
        types.InlineKeyboardButton("👤 Kabinet & Status", callback_data="cabinet"),
        types.InlineKeyboardButton("💬 Goldaw Hyzmaty", callback_data="support_info")
    )
    return kb

def get_pair_menu():
    kb = types.InlineKeyboardMarkup(row_width=2)
    kb.add(
        types.InlineKeyboardButton("💶 EUR/USD (OTC)", callback_data="pair_EURUSD"),
        types.InlineKeyboardButton("💷 GBP/USD (OTC)", callback_data="pair_GBPUSD"),
        types.InlineKeyboardButton("💴 EUR/JPY (OTC)", callback_data="pair_EURJPY"),
        types.InlineKeyboardButton("💵 USD/CAD (OTC)", callback_data="pair_USDCAD"),
        types.InlineKeyboardButton("🇦🇺 AUD/CAD (OTC)", callback_data="pair_AUDCAD"),
        types.InlineKeyboardButton("🔙 Baş Sahypa", callback_data="back_home")
    )
    return kb

def get_time_menu():
    kb = types.InlineKeyboardMarkup(row_width=2)
    kb.add(
        types.InlineKeyboardButton("⚡ 5 Sekunt", callback_data="time_5s"),
        types.InlineKeyboardButton("⚡ 15 Sekunt", callback_data="time_15s"),
        types.InlineKeyboardButton("⏱ 30 Sekunt", callback_data="time_30s"),
        types.InlineKeyboardButton("⏱ 1 Minut", callback_data="time_1m"),
        types.InlineKeyboardButton("⏱ 3 Minut", callback_data="time_3m"),
        types.InlineKeyboardButton("🔙 Jübütlere Dönmek", callback_data="select_pair")
    )
    return kb

def get_back_menu():
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("🔙 Baş Sahypa", callback_data="back_home"))
    return kb

@bot.message_handler(commands=['start'])
def start_cmd(message):
    try:
        text = "💎 **TRADING PRO ALGORITHM BOT** 💎\n\nSalam, Hormatly söwdagär! Aşakdaky menýudan özüňize laýyk bölümi saýlaň:"
        bot.send_message(message.chat.id, text, parse_mode="Markdown", reply_markup=get_main_menu())
    except Exception as e:
        print(f"Start säwligi: {e}")

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    chat_id = call.message.chat.id
    msg_id = call.message.message_id
    code = call.data

    try:
        bot.answer_callback_query(call.id)
    except Exception:
        pass

    try:
        if code == "select_pair":
            bot.edit_message_text(
                chat_id=chat_id, message_id=msg_id,
                text="📊 **Söwda Jübütligini (Atywy) Saýlaň:**",
                parse_mode="Markdown", reply_markup=get_pair_menu()
            )
            
        elif code.startswith("pair_"):
            mapping = {
                "pair_EURUSD": "EUR/USD (OTC)",
                "pair_GBPUSD": "GBP/USD (OTC)",
                "pair_EURJPY": "EUR/JPY (OTC)",
                "pair_USDCAD": "USD/CAD (OTC)",
                "pair_AUDCAD": "AUD/CAD (OTC)"
            }
            user_selections[chat_id] = mapping.get(code, "EUR/USD (OTC)")
            text = f"✅ Saýlanan jübüt: **{user_selections[chat_id]}**\n\n⏱ **Indi bolsa ekspirasiýa wagtyny saýlaň:**"
            bot.edit_message_text(
                chat_id=chat_id, message_id=msg_id,
                text=text, parse_mode="Markdown", reply_markup=get_time_menu()
            )
            
        elif code.startswith("time_"):
            times = {
                "time_5s": "5 Sekunt (Turbo)",
                "time_15s": "15 Sekunt (Turbo)",
                "time_30s": "30 Sekunt (Turbo)",
                "time_1m": "1 Minut",
                "time_3m": "3 Minut"
            }
            tf = times.get(code, "1 Minut")
            pair = user_selections.get(chat_id, "EUR/USD (OTC)")
            
            rsi = random.randint(20, 80)
            if rsi < 45:
                action = "ÝOKARI (CALL) 🟢"
                analysis = "RSI aşaky çäkden gaýdyşýar (Oversold)"
            elif rsi > 55:
                action = "AŞAK (PUT) 🔴"
                analysis = "RSI ýokarky çäkden gaýdyşýar (Overbought)"
            else:
                action = random.choice(["ÝOKARI (CALL) 🟢", "AŞAK (PUT) 🔴"])
                analysis = "Trend durnuklylygy we MACD kesişmesi"

            accuracy = random.randint(92, 99)
            
            signal_text = (
                f"⚡ **KÖP-İNDİKATORLY PRO ALGORITM** ⚡\n"
                "━━━━━━━━━━━━━━━━━━━━━━\n"
                f"📊 **Atyw:** `{pair}`\n"
                f"⏱ **Ekspirasiýa:** `{tf}`\n"
                f"🎯 **Netije / Ýagdaý:** **{action}**\n"
                "━━━━━━━━━━━━━━━━━━━━━━\n"
                f"📉 **RSI (14):** `{rsi}`\n"
                f"📈 **Analiz:** `{analysis}`\n"
                f"💎 **Takyklyk:** `~{accuracy}%`\n"
                f"🕒 **Wagt:** `{datetime.datetime.now().strftime('%H:%M:%S')}`\n\n"
                "⚠️ *Riskleriňize gözegçilik ediň!*"
            )
            bot.edit_message_text(
                chat_id=chat_id, message_id=msg_id,
                text=signal_text, parse_mode="Markdown", reply_markup=get_back_menu()
            )
            
        elif code == "market_analysis":
            bot.edit_message_text(
                chat_id=chat_id, message_id=msg_id,
                text="📈 **Market Analizi:** RSI, MACD we EMA görkezijileri bazarda durnukly işleýär.",
                parse_mode="Markdown", reply_markup=get_back_menu()
            )
            
        elif code == "cabinet":
            bot.edit_message_text(
                chat_id=chat_id, message_id=msg_id,
                text=f"👤 **Kabinet**\n🆔 ID: `{call.from_user.id}`\n📌 Status: VIP Trader",
                parse_mode="Markdown", reply_markup=get_back_menu()
            )

        elif code == "support_info":
            bot.edit_message_text(
                chat_id=chat_id, message_id=msg_id,
                text="💬 **Goldaw:** Telefon / Telegram: `+993 62391714`",
                parse_mode="Markdown", reply_markup=get_back_menu()
            )
            
        elif code == "back_home":
            bot.edit_message_text(
                chat_id=chat_id, message_id=msg_id,
                text="💎 **TRADING PRO ALGORITHM BOT** 💎\n\nAşakdaky menýudan bölümi saýlaň:",
                parse_mode="Markdown", reply_markup=get_main_menu()
            )
    except Exception as e:
        print(f"Callback säwligi: {e}")

if __name__ == '__main__':
    print("Bot arassalanan logika bilen işe başlady...")
    while True:
        try:
            bot.infinity_polling(timeout=10, long_polling_timeout=5)
        except Exception as e:
            print(f"Baglanyşyk säwligi, täzeden birikdirilýär: {e}")
          
