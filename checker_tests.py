from checker import *

tester = Checker()

# login tests
# Вход по правильному логину и паролю
if not tester.login(right_login, right_password):
	print('Right login passed')
else:
	print('Right login failed')
# Вход по неправильному логину и паролю
if tester.login(wrong_login, wrong_password):
	print('Wrong login passed')
else:
	print('Wrong login failed')

# get_count tests
# Если нет новых сообщений
if tester.get_count() == 0:
	print('Quantity == 0 passed')
else:
	print('Quantity == 0 failed')
# Если 2 новых сообщения
if tester.get_count() == 2:
	print('Quantity == 2 passed')
else:
	print('Quantity == 2 failed')

# get_last tests
# Список последних 3 сообщений
if len(tester.get_last(3)) == 3:
	print('Last messages list creating passed')
else:
	print('Last messages list creating failed')
# Получение сообщения с прикреплённым файлом
last = tester.get_last(1)
if len(last) == 1 and last[0].attachment == True:
	print('Message with file passed')
else:
	print('Message with file failed')
# Получение сообщения без прикреплённого файла
last = tester.get_last(1)
if len(last) == 1 and last[0].attachment == False:
	print('Message without file passed')
else:
	print('Message without file failed')