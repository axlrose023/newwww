from automation import WhatsAppAutomation
import schedule
import time


def job():
    driver_path = 'chromedriver.exe'
    profile_path = r'C:\Users\admin\PycharmProjects\pythonProject3'
    telegram_token = '7475564529:AAF_BrLewpDAzCP3dtugqi0OheUo6qH-S-A'
    chat_id = '395519902'

    whatsapp_bot = WhatsAppAutomation(driver_path, profile_path, telegram_token, chat_id)
    whatsapp_bot.setup_driver()
    whatsapp_bot.open_whatsapp()
    whatsapp_bot.send_plus_message()
    whatsapp_bot.close()


# Планирование задач
schedule.every().day.at("06:55").do(job)
schedule.every().day.at("23:51").do(job)

# Запуск цикла ожидания
while True:
    schedule.run_pending()
    time.sleep(1)
