from typing import final
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import os
import requests
import json

load_dotenv()

TOKEN: final = os.getenv('TELEGRAM_BOT_TOKEN')
BOT_USERNAME: final = os.getenv('TELEGRAM_BOT_USERNAME')

# Commands
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    create_user(update.message.chat.id, update.message.chat.first_name)
    await update.message.reply_text("¡Hola tal parece que me has invocado!")

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Los Comandos que tengo son: \n /start - Inicia el bot \n /help - Muestra los comandos disponibles \n /message - Envia un mensaje (Proyecyo en proceso) \n /chatid - Muestra el ID de chat conmigo")

async def message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Este comando esta en proceso de desarrollo")

async def chatid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Tu ID es: {update.message.chat.id}")


# Handle
def handle_text(text: str, who: str) -> str:
    processed: str = text.lower()

    if 'hola' in processed:
        return 'Hola un placer hablar contigo ' + who

    if 'adios' in processed:
        return 'Adios, espero verte pronto'

    if 'como estas' in processed:
        return 'Estoy bien, gracias por preguntar'

    return 'No entiendo lo que dices'

def create_user(id, name):
    with open('telegramIDs.json', 'r') as file:
        data = json.load(file)
        if not any(user['id'] == id for user in data):
            user = {
                'id': id,
                'name': name
            }
            data.append(user)
    with open('telegramIDs.json', 'w') as file:
        json.dump(data, file, indent=4)

def send_message_telegram(chat_id, text):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': text
    }
    response = requests.post(url, json=payload)
    return response

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    name = update.message.chat.first_name
    id = update.message.chat.id

    if 'group' in message_type:
        if BOT_USERNAME in text:
            name = update.message.from_user.first_name
            id = update.message.from_user.id
            processed: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_text(processed, f'{update.message.from_user.first_name}')
        else:
            return
    else:
        response: str = handle_text(text, f'{update.message.chat.first_name}')

    print(f'User({name}: {id}) in chat({message_type}) says: {text}')
    print(f'Bot: {response}')
    await update.message.reply_text(response)

async def errors(update: Update, context: ContextTypes):
    print(f'Update {update} caused error {context.error}')


def startBot():
    print('Bot is running...')
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('help', help))
    app.add_handler(CommandHandler('message', message))
    app.add_handler(CommandHandler('chatid', chatid))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Errors
    app.add_error_handler(errors)

    # Test

    # Polling
    print('Bot is polling...')
    app.run_polling(poll_interval=3)

if __name__ == '__main__':
    startBot()
