import time
import meta
import codecs as cod
from message import *
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class Checker:
    def __init__(self):
        # Открыть браузер
        self.bot = webdriver.Firefox()
        bot = self.bot
        # Открыть пронто
        self.window = bot.window_handles[-1]
        bot.get(meta.LINK)

    def exit(self):
        self.bot.refresh()

    def login(self, login, password):
        bot = self.bot
        bot.refresh()
        time.sleep(2)
        try:
            log = bot.find_element_by_id(meta.LOGIN)
            passw = bot.find_element_by_id(meta.PASSWORD)
            log.clear()
            passw.clear()
            log.send_keys(login)
            passw.send_keys(password)
            time.sleep(1)
            passw.send_keys(Keys.RETURN)
            for i in range(10):
                time.sleep(1)
                try:
                    if len(bot.find_elements_by_class_name(meta.MESSAGE_LIST)) > 0:
                        return False
                except:
                    continue
            return True
        except:
            return True

        return False

    def select_all_as_readed(self):
        try:
            self.bot.find_element_by_class_name(meta.UNREAD).click()
            self.bot.find_element_by_class_name(meta.ALL).click()
            self.bot.find_element_by_class_name(meta.READ).click()
        except:
            print('', end='')

    def get_count(self):
        # Смотрим количество новых сообщений
        quantity = 0
        for i in range(15):
            try:
                quantity = int(self.bot.find_element_by_class_name(meta.NEW_MESSAGES)\
                    .find_element_by_class_name(meta.QUANTITY).text)
            except:
                time.sleep(1)

        return quantity

    def get_last(self, quantity):
        bot = self.bot
        time.sleep(4)
        # Ищем список писем
        message_list = bot.find_elements_by_class_name(meta.MESSAGE_LIST)
        last_messages = []
        # Считываем новые сообщения
        for i in range(quantity):
            message_list[i].click()
            sender = message_list[i].find_element_by_class_name(meta.FROM).text
            theme = message_list[i].find_element_by_class_name(meta.THEME).text
            bot.switch_to.frame(bot.find_element_by_class_name(meta.CONTENT_FRAME))
            time.sleep(4)
            try:
                content = bot.find_element_by_class_name(meta.TEXT).text
            except:
                content = '<Не удалось получить текст письма>'
            attachment = len(bot.find_elements_by_class_name(meta.ATTACH)) > 0
            message = Message(sender, theme, content, attachment)
            bot.switch_to.default_content()
            last_messages.insert(0, message)

        return last_messages
