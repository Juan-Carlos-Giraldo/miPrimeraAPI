import threading
import asyncio
import server
import telegramBotTest as telegram

def run_server():
    server.app.run(debug=False, use_reloader=False)

def run_telegram_bot():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(telegram.startBot())

if __name__ == '__main__':
    server_thread = threading.Thread(target=run_server)
    bot_thread = threading.Thread(target=run_telegram_bot)

    server_thread.start()
    bot_thread.start()

    server_thread.join()
    bot_thread.join()