# === TO'LIQ ISHLAYDIGAN TELEGRAM GAME BOT KODI ===
# O'yinlar: Mines, Aviator, Dice
# Tugmalar: balans, hisob toldirish, pul chiqarish, bonus, referal

from keep_alive import keep_alive
import telebot from telebot import TeleBot, types
from telebot import types
import random
import threading
import time
import datetime

TOKEN = "8161107014:AAGBWEYVxie7-pB4-2FoGCPjCv_sl0yHogc"
bot = telebot.TeleBot(TOKEN)

user_balances = {}
addbal_state = {}
lucky_users = set()
user_settings = {}
user_games = {}
user_data = {}
uzcard = "5394 2822 2304 2232"
humo = "9860 1766 2141 5916"
user_mines_game = {}
user_mines_states = {}
user_aviator = {}
user_bonus_state = {}
user_positions = {}
withdraw_sessions = {}
user_states = {}
user_referred_by = {}
tic_tac_toe_states = {}
user_chicken_states = {}
multipliers = [1.08, 1.17, 1.27, 1.56, 1.89, 2.31, 2.8, 3.6, 5.5, 6.5]
azart_enabled = False
ADMIN_ID = 5815294733  # O'zingizning Telegram ID'ingiz
azart_enabled = True  # Dastlabki holat: yoqilgan

cancel_commands = [
    "/start", "/help", "/addbal", "/cancel",
    "❌ Bekor qilish", "🔙 Orqaga",
    "💰 Balance", "💳 Hisob toldirish", "🎲 Play Dice",
    "💣 Play Mines", "🛩 Play Aviator", "💸 Pul chiqarish",
    "🎁 Kunlik bonus", "👥 Referal link", "🎮 Play TicTacToe",
    "🐔 Play Chicken"  # 👈 Qo‘shildi
]


user_referred_by = {}  # Foydalanuvchi qaysi referal orqali kelganini saqlash uchun

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    args = message.text.split()

    if user_id not in user_balances:
        user_balances[user_id] = 3000  # boshlang‘ich balans

        if len(args) > 1:
            try:
                ref_id = int(args[1])
                if ref_id != user_id:
                    # Agar foydalanuvchi hali referal orqali bonus olmagan bo‘lsa
                    if user_id not in user_referred_by:
                        user_referred_by[user_id] = ref_id
                        user_balances[ref_id] = user_balances.get(ref_id, 0) + 1000
                        bot.send_message(ref_id, f"🎉 Siz yangi foydalanuvchini taklif qilib, 1000 so‘m bonus oldingiz!")
            except ValueError:
                pass
    else:
        # Foydalanuvchi mavjud bo‘lsa, referal kodi bilan bonus bermaymiz
        pass

    back_to_main_menu(message)



# === Asosiy menyuga qaytish funksiyasi ===
def back_to_main_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('💣 Play Mines', '🛩 Play Aviator')
    markup.add('🎲 Play Dice', '🎮 Play TicTacToe')
    markup.add('🐔 Play Chicken')  # 👈 Yangi tugma qo‘shildi
    markup.add('💰 Balance', '💸 Pul chiqarish')
    markup.add('💳 Hisob toldirish', '🎁 Kunlik bonus', '👥 Referal link')
    bot.send_message(message.chat.id, "🔙 Asosiy menyu:", reply_markup=markup)


@bot.message_handler(func=lambda m: m.text == "💰 Balance")
def show_balance(message):
    user_id = message.from_user.id
    bal = user_balances.get(user_id, 0)
    bot.send_message(message.chat.id, f"💰 Sizning balansingiz: {bal} so‘m")

cancel_commands = [
    "/start", "/help", "/addbal", "/cancel",
    "💰 Balance", "💳 Hisob toldirish", "🎲 Play Dice", "💣 Play Mines",
    "🛩 Play Aviator", "🎮 Play TicTacToe",  # ✅ Qo‘shildi
    "💸 Pul chiqarish", "🎁 Kunlik bonus", "👥 Referal link",
    "🔙 Orqaga"
]

@bot.message_handler(commands=['addbal'])
def addbal_start(message):
    if message.from_user.id != ADMIN_ID:
        return
    msg = bot.send_message(message.chat.id, "🆔 Foydalanuvchi ID raqamini kiriting:")
    bot.register_next_step_handler(msg, addbal_get_id)

def addbal_get_id(message):
    if message.text.startswith("/") or message.text in cancel_commands:
        bot.send_message(message.chat.id, "❌ Jarayon bekor qilindi. /addbal ni qayta bosing.")
        addbal_state.pop(message.from_user.id, None)
        return

    try:
        target_id = int(message.text)
        addbal_state[message.from_user.id] = {'target_id': target_id}
        msg = bot.send_message(message.chat.id, "💵 Qo‘shiladigan miqdorni kiriting:")
        bot.register_next_step_handler(msg, addbal_get_amount)
    except Exception:
        msg = bot.send_message(message.chat.id, "❌ Noto‘g‘ri ID. Iltimos, raqam kiriting:")
        bot.register_next_step_handler(msg, addbal_get_id)

def addbal_get_amount(message):
    if message.text.startswith("/") or message.text in cancel_commands:
        bot.send_message(message.chat.id, "❌ Jarayon bekor qilindi. /addbal ni qayta bosing.")
        addbal_state.pop(message.from_user.id, None)
        return

    try:
        amount = int(message.text)
        if amount <= 0:
            raise ValueError()
        admin_id = message.from_user.id
        target_id = addbal_state[admin_id]['target_id']

        user_balances[target_id] = user_balances.get(target_id, 0) + amount

        bot.send_message(admin_id, f"✅ {amount:,} so‘m foydalanuvchi {target_id} ga qo‘shildi.")

        try:
            bot.send_message(target_id, f"✅ Hisobingizga {amount:,} so‘m tushirildi!", parse_mode="HTML")
        except Exception:
            # Foydalanuvchiga xabar yuborishda xato bo‘lsa, e'tiborsiz qoldiramiz
            pass

        del addbal_state[admin_id]

    except Exception:
        msg = bot.send_message(message.chat.id, "❌ Noto‘g‘ri miqdor. Qaytadan raqam kiriting:")
        bot.register_next_step_handler(msg, addbal_get_amount)


@bot.message_handler(func=lambda m: m.text == "👥 Referal link")
def referal_link(message):
    uid = message.from_user.id
    username = bot.get_me().username
    link = f"https://t.me/{username}?start={uid}"
    bot.send_message(message.chat.id, f"👥 Referal linkingiz:\n{link}")

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("💳 Hisob toldirish")
    bot.send_message(message.chat.id, "Xush kelibsiz! Tanlang:", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text == "💳 Hisob toldirish")
def ask_amount(message):
    bot.send_message(message.chat.id, "💰 Qancha so‘m to‘ldirmoqchisiz?")
    bot.register_next_step_handler(message, ask_card_type)

def ask_card_type(message):
    try:
        amount = int(message.text)
        user_data[message.chat.id] = {'amount': amount}
        markup = types.InlineKeyboardMarkup()
        markup.add(
            types.InlineKeyboardButton("Uzcard", callback_data="card_uzcard"),
            types.InlineKeyboardButton("Humo", callback_data="card_humo")
        )
        bot.send_message(message.chat.id, "💳 Karta turini tanlang:", reply_markup=markup)
    except:
        bot.send_message(message.chat.id, "❗ Iltimos, raqam kiriting.")
        return ask_amount(message)

@bot.callback_query_handler(func=lambda call: call.data.startswith("card_"))
def send_card(call):
    user_id = call.from_user.id
    card_type = call.data.split("_")[1]
    user_data[user_id]['card_type'] = card_type

    card_number = uzcard if card_type == "uzcard" else humo
    amount = user_data[user_id]['amount']

    msg = (
        f"💳 To‘lov uchun karta:\n<b>{card_number}</b>\n\n"
        f"💰 Summa: {amount} so‘m\n\n"
        f"✅ To‘lovni amalga oshirgach, tugmani bosing."
    )

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("✅ To‘lov qildim", callback_data="paid"))
    bot.edit_message_text(chat_id=user_id, message_id=call.message.message_id,
                          text=msg, parse_mode="HTML", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "paid")
def user_paid(call):
    user_id = call.from_user.id
    data = user_data.get(user_id)
    if not data:
        bot.send_message(user_id, "Xatolik yuz berdi.")
        return

    amount = data['amount']
    card_type = data['card_type']
    username = call.from_user.username or "Yo‘q"

    msg = (
        f"📅 <b>Yangi to‘lov so‘rovi</b>\n"
        f"👤 Foydalanuvchi: @{username}\n"
        f"🆔 ID: <code>{user_id}</code>\n"
        f"💰 Summa: {amount} so‘m\n"
        f"💳 Karta: {card_type.upper()}"
    )

    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("✅ Tasdiqlash", callback_data=f"approve_{user_id}"),
        types.InlineKeyboardButton("❌ Rad etish", callback_data=f"reject_{user_id}")
    )
    bot.send_message(admin_id, msg, parse_mode="HTML", reply_markup=markup)
    bot.send_message(user_id, "🕐 So‘rovingiz yuborildi. Tekshiruv kutilmoqda...")

@bot.callback_query_handler(func=lambda call: call.data.startswith("approve_") or call.data.startswith("reject_"))
def handle_admin_action(call):
    user_id = int(call.data.split("_")[1])
    action = call.data.split("_")[0]
    data = user_data.get(user_id)

    if not data:
        bot.send_message(admin_id, "❗ Foydalanuvchi ma'lumoti topilmadi.")
        return

    amount = data['amount']

    if action == "approve":
        if user_id not in balances:
            balances[user_id] = 0
        balances[user_id] += amount

        bot.send_message(user_id, f"✅ To‘lov tasdiqlandi. Balansingiz {amount} so‘mga oshirildi.")
        bot.send_message(admin_id, f"💰 Hisob to‘ldirildi.\nFoydalanuvchi ID: <code>{user_id}</code>\nSumma: {amount} so‘m", parse_mode="HTML")
    else:
        bot.send_message(user_id, "❌ To‘lov rad etildi. Pul tushmagan bo‘lishi mumkin.")
        bot.send_message(admin_id, f"❌ To‘lov rad etildi. Foydalanuvchi ID: <code>{user_id}</code>", parse_mode="HTML")

    bot.answer_callback_query(call.id, "Yuborildi.")

@bot.message_handler(commands=['addbal'])
def add_balance(message):
    if message.from_user.id != admin_id:
        return

    try:
        _, user_id, amount = message.text.split()
        user_id = int(user_id)
        amount = int(amount)

        if user_id not in balances:
            balances[user_id] = 0
        balances[user_id] += amount

        bot.send_message(user_id, f"💰 Admin tomonidan balansingiz {amount} so‘mga to‘ldirildi.")
        bot.send_message(message.chat.id, f"✅ {user_id} ga {amount} so‘m qo‘shildi.")
    except:
        bot.send_message(message.chat.id, "❌ Xato format. To‘g‘ri foydalaning: /addbal user_id summa")


    bot.send_message(message.chat.id, text, parse_mode="HTML")
    # Botni sozlash, importlar, token va boshqalar

def back_to_main_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('💣 Play Mines', '🛩 Play Aviator')
    markup.add('🎲 Play Dice', '🎮 Play TicTacToe')
    markup.add('🐔 Play Chicken')  # 🆕 Chicken o‘yini tugmasi qo‘shildi
    markup.add('💰 Balance', '💳 Hisob toldirish')
    markup.add('💸 Pul chiqarish', '🎁 Kunlik bonus')
    markup.add('👥 Referal link')
    bot.send_message(message.chat.id, "🔙 Asosiy menyu:", reply_markup=markup)


# Yoki boshqa joyda
@bot.message_handler(func=lambda m: m.text == "🔙 Orqaga")
def go_back(message):
    back_to_main_menu(message)


@bot.message_handler(func=lambda m: m.text == "💸 Pul chiqarish")
def withdraw_step1(message):
    msg = bot.send_message(message.chat.id, "💵 Miqdorni kiriting (min 20000 so‘m):")
    bot.register_next_step_handler(msg, withdraw_step2)

def withdraw_step2(message):
    try:
        amount = int(message.text)
        user_id = message.from_user.id
        if amount < 20000:
            bot.send_message(message.chat.id, "❌ Minimal chiqarish miqdori 20000 so‘m.")
            return
        if user_balances.get(user_id, 0) < amount:
            bot.send_message(message.chat.id, "❌ Mablag‘ yetarli emas.")
            return
        withdraw_sessions[user_id] = amount
        msg = bot.send_message(message.chat.id, "💳 Karta yoki to‘lov usulini yozing:")
        bot.register_next_step_handler(msg, withdraw_step3)
    except:
        bot.send_message(message.chat.id, "❌ Noto‘g‘ri miqdor.")

# === SHU YERGA QO‘Y — withdraw_step3 ===
def withdraw_step3(message):
    user_id = message.from_user.id
    amount = withdraw_sessions.get(user_id)
    info = message.text.strip()

    # === Karta yoki to‘lov tizimi tekshiruvlari ===
    valid = False
    digits = ''.join(filter(str.isdigit, info))
    if len(digits) in [16, 19] and (digits.startswith('8600') or digits.startswith('9860') or digits.startswith('9989')):
        valid = True
    elif any(x in info.lower() for x in ['click', 'payme', 'uzcard', 'humo', 'apelsin']):
        valid = True

    if not valid:
        bot.send_message(message.chat.id, "❌ To‘lov usuli noto‘g‘ri kiritildi. Karta raqami (8600...) yoki servis nomini kiriting.")
        return

    user_balances[user_id] -= amount
    text = f"🔔 Yangi pul chiqarish so‘rovi!\n👤 @{message.from_user.username or 'no_username'}\n🆔 ID: {user_id}\n💵 Miqdor: {amount} so‘m\n💳 To‘lov: {info}"
    bot.send_message(ADMIN_ID, text)
    bot.send_message(message.chat.id, "✅ So‘rov yuborildi, kuting.")
    del withdraw_sessions[user_id]

@bot.message_handler(commands=['lucky_list'])
def show_lucky_list(message):
    if message.from_user.id != ADMIN_ID:
        return

    if not lucky_users:
        bot.send_message(message.chat.id, "📭 Lucky foydalanuvchilar yo‘q.")
    else:
        users = "\n".join([f"🆔 {uid}" for uid in lucky_users])
        bot.send_message(message.chat.id, f"🎯 Lucky foydalanuvchilar ro‘yxati:\n{users}")


@bot.message_handler(func=lambda m: m.text == "🎮 Play TicTacToe")
def start_tictactoe_bet(message):
    user_id = message.from_user.id
    msg = bot.send_message(message.chat.id, "🎯 Stavka miqdorini kiriting (min 1000 so‘m):")
    bot.register_next_step_handler(msg, process_ttt_bet)

def process_ttt_bet(message):
    user_id = message.from_user.id
    try:
        stake = int(message.text)
        if stake < 1000:
            bot.send_message(message.chat.id, "❌ Minimal stavka 1000 so‘m.")
            return
        if user_balances.get(user_id, 0) < stake:
            bot.send_message(message.chat.id, "❌ Mablag‘ yetarli emas.")
            return
    except:
        bot.send_message(message.chat.id, "❌ To‘g‘ri raqam kiriting.")
        return

    user_balances[user_id] -= stake
    tic_tac_toe_states[user_id] = {
        "board": [" "] * 9,
        "stake": stake
    }
    board = tic_tac_toe_states[user_id]["board"]
    bot.send_message(message.chat.id, "🎮 O‘yin boshlandi! Siz 'X' bilan o‘ynaysiz. Katakni tanlang:", reply_markup=board_to_markup(board))

def board_to_markup(board):
    markup = types.InlineKeyboardMarkup(row_width=3)
    buttons = []
    for i, cell in enumerate(board):
        text = cell if cell != " " else "⬜"
        buttons.append(types.InlineKeyboardButton(text, callback_data=f"ttt_{i}"))
    markup.add(*buttons)
    return markup

def check_winner(board, player):
    wins = [[0,1,2], [3,4,5], [6,7,8],
            [0,3,6], [1,4,7], [2,5,8],
            [0,4,8], [2,4,6]]
    return any(all(board[pos] == player for pos in line) for line in wins)

def is_board_full(board):
    return all(cell != " " for cell in board)

def find_best_move(board):
    # Agar bot yutishi mumkin bo'lsa, o'sha joyga boradi
    for i in range(9):
        if board[i] == " ":
            board[i] = "O"
            if check_winner(board, "O"):
                board[i] = " "
                return i
            board[i] = " "
    # Agar foydalanuvchi yutishi mumkin bo'lsa, bloklaydi
    for i in range(9):
        if board[i] == " ":
            board[i] = "X"
            if check_winner(board, "X"):
                board[i] = " "
                return i
            board[i] = " "
    # Aks holda random
    empty = [i for i, c in enumerate(board) if c == " "]
    return random.choice(empty)

@bot.callback_query_handler(func=lambda call: call.data.startswith("ttt_"))
def ttt_handle_move(call):
    user_id = call.from_user.id
    state = tic_tac_toe_states.get(user_id)
    if not state:
        bot.answer_callback_query(call.id, "O'yin topilmadi.")
        return

    board = state["board"]
    idx = int(call.data.split("_")[1])
    if board[idx] != " ":
        bot.answer_callback_query(call.id, "Bu katak band.")
        return

    board[idx] = "X"
    if check_winner(board, "X"):
        prize = int(state["stake"] * 1.5)
        user_balances[user_id] += prize
        bot.edit_message_text(f"🌟 Siz yutdingiz! {prize} so‘m oldingiz. (1.5x)", call.message.chat.id, call.message.message_id)
        tic_tac_toe_states.pop(user_id)
        return

    if is_board_full(board):
        refund = int(state["stake"] * 0.5)
        user_balances[user_id] += refund
        bot.edit_message_text(f"⚖️ Durang. Faqat {refund} so‘m qaytdi. (50%)", call.message.chat.id, call.message.message_id)
        tic_tac_toe_states.pop(user_id)
        return

    bot_move = find_best_move(board)
    board[bot_move] = "O"
    if check_winner(board, "O"):
        bot.edit_message_text("😞 Bot yutdi! Siz stavkani yo‘qotdingiz.", call.message.chat.id, call.message.message_id)
        tic_tac_toe_states.pop(user_id)
        return

    if is_board_full(board):
        refund = int(state["stake"] * 0.5)
        user_balances[user_id] += refund
        bot.edit_message_text(f"⚖️ Durang. Faqat {refund} so‘m qaytdi. (50%)", call.message.chat.id, call.message.message_id)
        tic_tac_toe_states.pop(user_id)
        return

    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=board_to_markup(board))
    bot.answer_callback_query(call.id, "Yurishingiz qabul qilindi!")

@bot.message_handler(func=lambda m: m.text == "🎁 Kunlik bonus")
def daily_bonus(message):
    user_id = message.from_user.id
    today = datetime.date.today()
    if user_bonus_state.get(user_id) == today:
        bot.send_message(message.chat.id, "🎁 Siz bugun bonus oldingiz.")
        return
    bonus = random.randint(1000, 5000)
    user_balances[user_id] = user_balances.get(user_id, 0) + bonus
    user_bonus_state[user_id] = today
    bot.send_message(message.chat.id, f"🎉 Sizga {bonus} so‘m bonus berildi!")

@bot.message_handler(func=lambda m: m.text == "🎲 Play Dice")
def dice_start(message):
    msg = bot.send_message(message.chat.id, "🎯 Stavka miqdorini kiriting:")
    bot.register_next_step_handler(msg, dice_process)

def dice_process(message):
    if message.text == "🔙 Orqaga":
        return back_to_main_menu(message)
    try:
        user_id = message.from_user.id
        stake = int(message.text)
        if user_balances.get(user_id, 0) < stake:
            bot.send_message(message.chat.id, "❌ Mablag‘ yetarli emas.")
            return
        user_balances[user_id] -= stake
        bot.send_message(message.chat.id, "🎲 Qaytarilmoqda...")
        time.sleep(2)
        dice = random.randint(1, 6)
        if dice <= 2:
            win = 0
        elif dice <= 4:
            win = stake
        else:
            win = stake * 2
        user_balances[user_id] += win
        bot.send_dice(message.chat.id)
        time.sleep(3)
        bot.send_message(
            message.chat.id,
            f"🎲 Natija: {dice}\n"
            f"{'✅ Yutdingiz!' if win > stake else '❌ Yutqazdingiz.'}\n"
            f"💵 Yutuq: {win} so‘m"
        )
    except:
        bot.send_message(message.chat.id, "❌ Noto‘g‘ri stavka.")

@bot.message_handler(commands=['make_lucky'])
def make_lucky(message):
    if message.from_user.id != ADMIN_ID:
        return bot.send_message(message.chat.id, "⛔ Sizda ruxsat yo‘q.")

    parts = message.text.strip().split()
    if len(parts) < 2:
        return bot.send_message(message.chat.id, "❗ Foydalanuvchi ID raqamini yozing. Masalan: /make_lucky 12345678")

    try:
        user_id = int(parts[1])
        lucky_users.add(user_id)
        bot.send_message(message.chat.id, f"✅ Foydalanuvchi {user_id} lucky ro‘yxatiga qo‘shildi.")
    except ValueError:
        bot.send_message(message.chat.id, "❌ ID raqami noto‘g‘ri.")

@bot.message_handler(commands=['remove_lucky'])
def remove_lucky(message):
    if message.from_user.id != ADMIN_ID:
        return bot.send_message(message.chat.id, "⛔ Sizda ruxsat yo‘q.")

    parts = message.text.strip().split()
    if len(parts) < 2:
        return bot.send_message(message.chat.id, "❗ Foydalanuvchi ID raqamini yozing. Masalan: /remove_lucky 12345678")

    try:
        user_id = int(parts[1])
        if user_id in lucky_users:
            lucky_users.remove(user_id)
            bot.send_message(message.chat.id, f"🗑 Foydalanuvchi {user_id} lucky ro‘yxatidan o‘chirildi.")
        else:
            bot.send_message(message.chat.id, f"⚠️ {user_id} lucky ro‘yxatida yo‘q.")
    except ValueError:
        bot.send_message(message.chat.id, "❌ ID raqami noto‘g‘ri.")

@bot.message_handler(commands=['lucky_list'])
def lucky_list(message):
    if message.from_user.id != ADMIN_ID:
        return bot.send_message(message.chat.id, "⛔ Sizda ruxsat yo‘q.")

    if not lucky_users:
        return bot.send_message(message.chat.id, "📭 Lucky ro‘yxati bo‘sh.")

    text = "📋 Lucky foydalanuvchilar ro‘yxati:\n"
    for uid in lucky_users:
        text += f"🆔 {uid}\n"
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    if user_id not in user_balances:
        user_balances[user_id] = 0  # balansni 0 dan boshlaymiz

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("💣 Play Mines", "💰 Balance")
    bot.send_message(user_id, "🎮 Welcome! Choose an option:", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text == "💰 Balance")
def check_balance(message):
    user_id = message.from_user.id
    balance = user_balances.get(user_id, 0)
    bot.send_message(user_id, f"💼 Your balance: {balance} so'm")

@bot.message_handler(func=lambda m: m.text == "💣 Play Mines")
def ask_stake(message):
    user_id = message.from_user.id
    bot.send_message(user_id, "💵 Enter your stake amount (minimum 1000 so'm):")
    user_states[user_id] = "awaiting_stake"

@bot.message_handler(func=lambda m: m.from_user.id in user_states and user_states[m.from_user.id] == "awaiting_stake")
def handle_stake(message):
    user_id = message.from_user.id
    try:
        stake = int(message.text)
        if stake < 1000:
            bot.send_message(user_id, "❌ Minimal stake is 1000 so'm. Try again.")
            return
        if user_balances.get(user_id, 0) < stake:
            bot.send_message(user_id, "❌ Not enough balance.")
            return

        user_balances[user_id] -= stake
        cells = list(range(25))
        bombs = random.sample(cells, 5)
        user_mines_game[user_id] = {
            'bombs': bombs,
            'opened': [],
            'stake': stake
        }
        user_states.pop(user_id, None)
        bot.send_message(user_id, f"🎮 Game started with stake: {stake} so'm. Good luck!")
        send_mines_grid(user_id)

    except ValueError:
        bot.send_message(user_id, "❗ Please enter a valid number.")

def send_mines_grid(user_id):
    game = user_mines_game[user_id]
    markup = types.InlineKeyboardMarkup(row_width=5)
    buttons = []

    for i in range(25):
        if i in game['opened']:
            btn = types.InlineKeyboardButton("💵", callback_data=f"noop")
        else:
            btn = types.InlineKeyboardButton("⬜️", callback_data=f"mine_{i}")
        buttons.append(btn)

    for i in range(0, 25, 5):
        markup.row(*buttons[i:i+5])

    markup.add(types.InlineKeyboardButton("💸 Cash Out", callback_data="cashout"))
    bot.send_message(user_id, "🔍 Choose a cell:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("mine_") or call.data == "cashout")
def handle_mines_callback(call):
    user_id = call.from_user.id
    if user_id not in user_mines_game:
        bot.answer_callback_query(call.id, "❌ No active game.")
        return

    game = user_mines_game[user_id]

    if call.data == "cashout":
        count = len(game['opened'])
        if count == 0:
            bot.answer_callback_query(call.id, "❌ Open at least one cell.")
            return
        multiplier = multipliers[min(count - 1, len(multipliers) - 1)]
        win = round(game['stake'] * multiplier)
        user_balances[user_id] += win
        bot.edit_message_text(f"✅ Cashed out with x{multiplier}\n💰 You won: {win} so'm", call.message.chat.id, call.message.message_id)
        del user_mines_game[user_id]
        return

    index = int(call.data.split("_")[1])
    if index in game['opened']:
        bot.answer_callback_query(call.id, "❗ Already opened.")
        return

    if index in game['bombs']:
        bot.edit_message_text("💥 You hit a bomb! ❌ You lost.", call.message.chat.id, call.message.message_id)
        del user_mines_game[user_id]
        return

    game['opened'].append(index)
    send_mines_grid(user_id)


# === AVIATOR o'yini funksiyasi ===
@bot.message_handler(func=lambda m: m.text == "🛩 Play Aviator")
def play_aviator(message):
    user_id = message.from_user.id
    if user_id in user_aviator:
        bot.send_message(message.chat.id, "⏳ Avvalgi Aviator o‘yini tugamagani uchun kuting.")
        return
    msg = bot.send_message(message.chat.id, "🎯 Stavka miqdorini kiriting (min 1000 so‘m):")
    bot.register_next_step_handler(msg, process_aviator_stake)

def process_aviator_stake(message):
    if message.text == "🔙 Orqaga":
        return back_to_main_menu(message)
    try:
        user_id = message.from_user.id
        stake = int(message.text)
        if stake < 1000:
            bot.send_message(message.chat.id, "❌ Minimal stavka 1000 so‘m.")
            return
        if user_balances.get(user_id, 0) < stake:
            bot.send_message(message.chat.id, "❌ Yetarli balans yo‘q.")
            return
        user_balances[user_id] -= stake
        user_aviator[user_id] = {
            'stake': stake,
            'multiplier': 1.0,
            'chat_id': message.chat.id,
            'message_id': None,
            'stopped': False
        }
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🛑 STOP", callback_data="aviator_stop"))
        msg = bot.send_message(message.chat.id, f"🛫 Boshlanmoqda... x1.00", reply_markup=markup)
        user_aviator[user_id]['message_id'] = msg.message_id
        threading.Thread(target=run_aviator_game, args=(user_id,)).start()
    except:
        bot.send_message(message.chat.id, "❌ Xatolik. Raqam kiriting.")


def run_aviator_game(user_id):
    data = user_aviator.get(user_id)
    if not data:
        return
    chat_id = data['chat_id']
    message_id = data['message_id']
    stake = data['stake']
    multiplier = data['multiplier']
    for _ in range(30):
        if user_aviator.get(user_id, {}).get('stopped'):
            win = int(stake * multiplier)
            user_balances[user_id] += win
            bot.edit_message_text(f"🛑 To‘xtatildi: x{multiplier}\n✅ Yutuq: {win} so‘m", chat_id, message_id)
            del user_aviator[user_id]
            return
        time.sleep(1)
        multiplier = round(multiplier + random.uniform(0.15, 0.4), 2)
        chance = random.random()
        if (multiplier <= 1.6 and chance < 0.3) or (1.6 < multiplier <= 2.4 and chance < 0.15) or (multiplier > 2.4 and chance < 0.1):
            bot.edit_message_text(f"💥 Portladi: x{multiplier}\n❌ Siz yutqazdingiz.", chat_id, message_id)
            del user_aviator[user_id]
            return
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🛑 STOP", callback_data="aviator_stop"))
        try:
            bot.edit_message_text(f"🛩 Ko‘tarilmoqda... x{multiplier}", chat_id, message_id, reply_markup=markup)
        except:
            pass
        user_aviator[user_id]['multiplier'] = multiplier
@bot.callback_query_handler(func=lambda call: call.data == "aviator_stop")
def aviator_stop(call):
    user_id = call.from_user.id
    if user_id in user_aviator:
        user_aviator[user_id]['stopped'] = True
        bot.answer_callback_query(call.id, "🛑 O'yin to'xtatildi, pulingiz qaytarildi.")


CHICKEN = "🐔"
PASSED = "✅"
UNLOCKED = "🔓"
LOCKED = "🔒"
BOMB = "💥"

azart_enabled = True  # Agar admin sozlasa, global azart yoqiladi

@bot.message_handler(func=lambda m: m.text == "🐔 Play Chicken")
def start_chicken(message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    msg = bot.send_message(chat_id, "💸 Stavka miqdorini kiriting (min 1000 so‘m):")
    bot.register_next_step_handler(msg, lambda m: process_chicken_stake(m, user_id))

def process_chicken_stake(message, user_id):
    chat_id = message.chat.id
    try:
        stake = int(message.text)
        if stake < 1000:
            return bot.send_message(chat_id, "❌ Minimal stavka 1000 so‘m.")
        if user_balances.get(user_id, 0) < stake:
            return bot.send_message(chat_id, "❌ Mablag‘ yetarli emas.")
    except:
        return bot.send_message(chat_id, "❌ Raqam kiriting.")

    user_balances[user_id] -= stake
    user_chicken_states[user_id] = {
        'pos': 0,
        'stake': stake,
        'multiplier': 1.0,
        'alive': True
    }

    send_chicken_grid(chat_id, user_id)

def send_chicken_grid(chat_id, user_id):
    state = user_chicken_states[user_id]
    pos = state['pos']
    cells = []
    markup = types.InlineKeyboardMarkup(row_width=5)

    for i in range(10):
        if i < pos:
            cells.append(PASSED)
            markup.add(types.InlineKeyboardButton(PASSED, callback_data="ignore"))
        elif i == pos:
            cells.append(CHICKEN)
            markup.add(types.InlineKeyboardButton(CHICKEN, callback_data="ignore"))
        elif i == pos + 1:
            cells.append(UNLOCKED)
            markup.add(types.InlineKeyboardButton(UNLOCKED, callback_data=f"chicken_jump_{i}"))
        else:
            cells.append(LOCKED)
            markup.add(types.InlineKeyboardButton(LOCKED, callback_data="ignore"))

    pot_win = int(state['stake'] * state['multiplier'])

    markup.add(types.InlineKeyboardButton("💸 Pulni yechib olish", callback_data="chicken_cashout"))

    line = " > ".join(cells)
    bot.send_message(chat_id,
        f"🐔 Chicken Road o‘yini\n\n"
        f"{line}\n\n"
        f"📈 Koef: x{round(state['multiplier'], 2)}\n"
        f"💰 Potensial yutuq: {pot_win} so‘m\n\n"
        f"🐔 Keyingi katakka sakrash uchun 🔓 tugmasini bosing yoki pulni yeching.",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith("chicken_"))
def handle_chicken(call):
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    state = user_chicken_states.get(user_id)

    if not state or not state['alive']:
        return bot.answer_callback_query(call.id, "⛔ O‘yin mavjud emas.")

    if call.data == "chicken_cashout":
        win = int(state['stake'] * state['multiplier'])
        user_balances[user_id] += win
        user_chicken_states.pop(user_id)
        return bot.edit_message_text(f"✅ Pul chiqarildi! Yutuq: {win:,} so‘m", chat_id, call.message.message_id)

    if call.data.startswith("chicken_jump_"):
        target = int(call.data.split("_")[-1])
        pos = state['pos']
        if target != pos + 1:
            return bot.answer_callback_query(call.id, "⛔ Faqat yonidagi katakka sakrashingiz mumkin.")

        # Azart xavfi
        if azart_enabled:
            risk = 0.6 + (pos * 0.08)
        else:
            risk = 0.9 + (pos * 0.3)

        if random.random() < risk:
            line = []
            for i in range(10):
                if i == target:
                    line.append(BOMB)
                elif i < pos:
                    line.append(PASSED)
                elif i == pos:
                    line.append(CHICKEN)
                else:
                    line.append(LOCKED)
            return bot.edit_message_text(
                f"💥 Boom! Bombaga tushdi!\nStavka yo‘qotildi.\n\n{' > '.join(line)}",
                chat_id, call.message.message_id
            )

        # Xavfsiz sakrash
        state['pos'] += 1
        state['multiplier'] = multipliers[state['pos']]
        if state['pos'] == 9:
            win = int(state['stake'] * state['multiplier'])
            user_balances[user_id] += win
            line = get_final_chicken_line(state['pos'])
            user_chicken_states.pop(user_id)
            return bot.edit_message_text(
                f"🎉 Tovuq manzilga yetdi! Yutuq: {win:,} so‘m\n\n{line}",
                chat_id, call.message.message_id
            )
        send_chicken_grid(chat_id, user_id)

def get_final_chicken_line(pos):
    cells = []
    for i in range(10):
        if i < pos:
            cells.append(PASSED)
        elif i == pos:
            cells.append(CHICKEN)
        else:
            cells.append(LOCKED)
    return " > ".join(cells)


print("Bot ishga tushdi...")
keep_alive()
bot.polling(none_stop=True)
