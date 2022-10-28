from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext
import os
from telegram_response import BackendClient

token = os.environ["TG_TOKEN"]
updater = Updater(token=token, use_context=True)
keybord= [["Найти слово", "Добавить слово", "Изменить слово", "Удалить слово", "Назад"]]
back_client = BackendClient()

#system_func
def main_keybord(keybord: list):
    return ReplyKeyboardMarkup(keybord, resize_keyboard=True)

def start_menu(update: Update, context: CallbackContext):
    user_name = update["message"]["chat"]["username"]
    update.message.reply_text(f"Hello {user_name}", reply_markup=main_keybord(keybord))

def back(update: Update, context: CallbackContext):
    return ConversationHandler.END

#add_handler
def add_word(update: Update, context: CallbackContext):
    update.message.reply_text("Введите слово")
    return 1

def first_add_response(update: Update, context: CallbackContext):
    context.user_data["dictionary"] = {"word": update.message.text}
    if context.user_data["dictionary"]["word"] == "Назад":
        return ConversationHandler.END
    update.message.reply_text("Введите перевод или описание")
    return 2

def second_add_response(update: Update, context: CallbackContext):
    context.user_data["dictionary"]["description"] = update.message.text
    if context.user_data["dictionary"]["description"] == "Назад":
        return ConversationHandler.END
    word = context.user_data["dictionary"]["word"].lower()
    description = context.user_data["dictionary"]["description"].lower()
    data = back_client.add(word=word, description=description)
    if data == None:
        update.message.reply_text("Слово уже добавлено")
        return ConversationHandler.END
    update.message.reply_text("Добавлено")
    return ConversationHandler.END

#find_handler
def find_word(update: Update, context: CallbackContext):
    update.message.reply_text("Введите слово")
    return 1

def first_find_response(update: Update, context: CallbackContext):
    context.user_data["dictionary"] = {"word": update.message.text}
    if context.user_data["dictionary"]["word"] == "Назад":
        return ConversationHandler.END
    word = context.user_data["dictionary"]["word"].lower()
    data = back_client.search(word=word)
    if data["description"] == None:
        update.message.reply_text(f"Слово не найдено")
        return ConversationHandler.END
    update.message.reply_text(data["description"])
    return ConversationHandler.END

#change_word
def change_word(update: Update, context: CallbackContext):
    update.message.reply_text("Введите слово")
    return 1

def first_change_response(update: Update, context: CallbackContext):
    context.user_data["dictionary"] = {"word": update.message.text}
    if context.user_data["dictionary"]["word"] == "Назад":
        return ConversationHandler.END
    update.message.reply_text("Введите новое слово")
    return 2

def second_change_response(update: Update, context: CallbackContext):
    context.user_data["dictionary"]["new_word"] = update.message.text
    if context.user_data["dictionary"]["new_word"] == "Назад":
        return ConversationHandler.END
    update.message.reply_text("Введите перевод или описание")
    return 3

def third_change_response(update: Update, context: CallbackContext):
    context.user_data["dictionary"]["new_description"] = update.message.text
    if context.user_data["dictionary"]["new_description"] == "Назад":
        return ConversationHandler.END
    word = context.user_data["dictionary"]["word"].lower()
    new_word = context.user_data["dictionary"]["new_word"].lower()
    new_description = context.user_data["dictionary"]["new_description"].lower()
    data = back_client.change(word=word,
                                new_word=new_word,
                                new_description=new_description)
    if data == None:
        update.message.reply_text("Слово не найдено или измениния которые вы хотите внести уже есть")
        return ConversationHandler.END
    update.message.reply_text("Изменено")
    return ConversationHandler.END

#delete_handler
def delete_word(update: Update, context: CallbackContext):
    update.message.reply_text("Введите слово")
    return 1

def first_delete_response(update: Update, context: CallbackContext):
    context.user_data["dictionary"] = {"word": update.message.text}
    if context.user_data["dictionary"]["word"] == "Назад":
        return ConversationHandler.END
    data = back_client.delete(context.user_data["dictionary"]["word"].lower())
    if data == None:
        update.message.reply_text("Слово удалено")
        return ConversationHandler.END


def main():
    dp = updater.dispatcher

    add_handler = ConversationHandler(entry_points=[MessageHandler(Filters.regex("^(Добавить слово)$"), add_word)],
                                      states={1: [MessageHandler(Filters.text & ~Filters.command, first_add_response)],
                                              2: [MessageHandler(Filters.text & ~Filters.command, second_add_response)]},
                                      fallbacks=[CommandHandler("back", back),
                                                 MessageHandler(Filters.photo | Filters.video | Filters.document | Filters.location | Filters.voice, back)])


    find_handler = ConversationHandler(entry_points=[MessageHandler(Filters.regex("^(Найти слово)$"), find_word)],
                                       states={1: [MessageHandler(Filters.text & ~Filters.command, first_find_response)]},
                                       fallbacks=[CommandHandler("back", back),
                                                  MessageHandler(Filters.photo | Filters.video | Filters.document | Filters.location | Filters.voice, back)])


    change_handler = ConversationHandler(entry_points=[MessageHandler(Filters.regex("^(Изменить слово)$"), change_word)],
                                         states={1: [MessageHandler(Filters.text & ~Filters.command, first_change_response)],
                                                 2: [MessageHandler(Filters.text & ~Filters.command, second_change_response)],
                                                 3: [MessageHandler(Filters.text & ~Filters.command, third_change_response)]},
                                         fallbacks=[CommandHandler("back", back),
                                                    MessageHandler(Filters.photo | Filters.video | Filters.document | Filters.location | Filters.voice, back)])


    delete_handler = ConversationHandler(entry_points=[MessageHandler(Filters.regex("^(Удалить слово)$"), delete_word)],
                                         states={1: [MessageHandler(Filters.text & ~Filters.command, first_delete_response)]},
                                         fallbacks=[CommandHandler("back", back),
                                                    MessageHandler(Filters.photo | Filters.video | Filters.document | Filters.location | Filters.voice, back)])

    dp.add_handler(add_handler)
    dp.add_handler(find_handler)
    dp.add_handler(change_handler)
    dp.add_handler(delete_handler)
    dp.add_handler(CommandHandler("start", start_menu))
    dp.add_handler(MessageHandler(Filters.regex("^(Назад)$"), back))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
