import os
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time


class WhatsAppAutomation:
    def __init__(self, driver_path, profile_path, telegram_token, chat_id):
        self.driver_path = driver_path
        self.profile_path = profile_path
        self.telegram_token = telegram_token
        self.chat_id = chat_id
        self.driver = None

    def setup_driver(self):
        # Проверка, существует ли профиль
        if not os.path.exists(self.profile_path):
            print(f"Профиль не найден, создается новый профиль по пути: {self.profile_path}")
            os.makedirs(self.profile_path)

        service = Service(self.driver_path)
        options = webdriver.ChromeOptions()
        options.add_argument(f'user-data-dir={self.profile_path}')
        self.driver = webdriver.Chrome(service=service, options=options)

    def open_whatsapp(self):
        self.driver.get('https://web.whatsapp.com')
        time.sleep(5)  # Даем время на загрузку страницы

    def send_plus_message(self):
        try:
            # Поиск и нажатие на первый чат
            first_chat = self.driver.find_element(By.XPATH,
                                                  '/html/body/div[1]/div/div/div[2]/div[3]/div/div[3]/div[1]/div/div/div[1]/div/div')
            first_chat.click()
            time.sleep(2)  # Даем время на загрузку чата

            # Поиск поля ввода сообщения и отправка плюса
            message_box = self.driver.find_element(By.XPATH,
                                                   '/html/body/div[1]/div/div/div[2]/div[4]/div/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]/p')
            message_box.click()
            message_box.send_keys('+')
            message_box.send_keys(Keys.ENTER)
            print("Сообщение с плюсом отправлено!")

            # Уведомление об успешной отправке
            self.send_telegram_message("Сообщение '+' отправлено в WhatsApp!")

        except Exception as e:
            print(f"Произошла ошибка: {e}")
            self.send_telegram_message("Ошибка: сообщение '+' не было отправлено в WhatsApp!")

    def send_telegram_message(self, message_text):
        telegram_url = f"https://api.telegram.org/bot{self.telegram_token}/sendMessage"
        response = requests.post(telegram_url,
                                 data={'chat_id': self.chat_id, 'text': message_text})
        if response.status_code == 200:
            print("Уведомление отправлено в Telegram!")
        else:
            print(f"Ошибка при отправке уведомления в Telegram: {response.status_code}")

    def close(self):
        if self.driver:
            time.sleep(5)
            self.driver.quit()
