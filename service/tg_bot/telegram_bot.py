from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext
import os

token = os.environ["TG_TOKEN"]
updater = Updater(token=token, use_context=True)
keybord= [["Найти слово", "Добавить слово", "Изменить слово", "Удалить слово", "Назад"]]

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
    #Если такое слово уже есть в базе то сообщаем об этом
    update.message.reply_text("Введите переводи или описание")
    return 2

def second_add_response(update: Update, context: CallbackContext):
    context.user_data["dictionary"]["description"] = update.message.text
    if context.user_data["dictionary"]["description"] == "Назад":
        return ConversationHandler.END
    #Добавляем слово и описание в базу
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
    #Обработка опечатки
    #Возвращаем описание из базы
    update.message.reply_text("описание\перевод слова которе мы нашли")
    return ConversationHandler.END

#change_word
def change_word(update: Update, context: CallbackContext):
    update.message.reply_text("Введите слово")
    return 1

def first_change_response(update: Update, context: CallbackContext):
    context.user_data["dictionary"] = {"word": update.message.text}
    if context.user_data["dictionary"]["word"] == "Назад":
        return ConversationHandler.END
    #Проверка наличия слова в базе
    #Если слова нету то обрабатываем исключение и выходим
    update.message.reply_text("Введите новый переводи или описание")
    return 2

def second_change_response(update: Update, context: CallbackContext):
    context.user_data["dictionary"]["description"] = update.message.text
    if context.user_data["dictionary"]["description"] == "Назад":
        return ConversationHandler.END
    #Изменяем слово в базе
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
    # Ищем слово в базе
    # Если слова нет то сообщаем об этом
    # Если есть то сообщаем что удалили ну и собсна удаляем
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
                                                 2: [MessageHandler(Filters.text & ~Filters.command, second_change_response)]},
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
