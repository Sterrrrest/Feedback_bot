Описание
=
Данный проект запускает ботов в Тулуграм и ВКонтакте. И с помощью GoogleFlow отвечает на заданные вопросы.

Установка
=
Зарегистрировать бота в ТГ и получить токен  [Как регистрировать бота](bit.ly/47ELQuZ).

Создайте группу в ВК и в настройках группы получите АПИ.

Создайте проект на [DialogFlow](https://console.cloud.google.com/home/dashboard?project=graphical-bus-431909-u0)

Создайте [Агента](https://dialogflow.cloud.google.com/) (это что-то вроде бота)

Переменные окружения
=
Разверните окружение:

```python3 -m venv venv```

Зайдите в него:

```source venv/bin/activate```

Установите требуемые библиотеки:

```pip install -r requirements.txt```


Примеры запуска скриптов
=

Автоматически установить вопросы в DialogFlow:
```
python3 create_intent. py - u https://dvmn.org/media/filer_public/a7/db/a7db66c0-1259-4dac-9726-2d1fa9c44f20/questions.json
```

Запустить бота в Телеграм:

```
python3 tg_bot.py
```

Запустить бота в ВК:
```
python3 vk_bot.py
```

Бот отвечает на доступные вопросы из DialogFlow. На остальные вопросы молчит и ждет оператора.


