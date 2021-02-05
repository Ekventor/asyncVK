    asyncVK – асинхронный фреймворк для создания ботов ВК. Преимущества: удобство, скорость выигрываемая за счёт асинхронности. 
Бот создаётся за счёт пяти структурных единиц: 
1) Bot – это самая главная структурная единица. Это собственно сам бот, который подаёт ивенты     обработчикам.
2) Handler – эта структурная единица отвечает за обработку ивентов. 
3) Dispatcher – эта структурная единица отвечает за взаимодействие с ВК (ответы на сообщения, добавление комментариев). Она автоматически настраивается хандлерами.
4) Keyboard – это второстепенная структурная единица. Она отвечает за создание кнопок в ВК.
5) Condition (Condition, And, Or) – эта структурная единица отвечает за условия. С помощью неё можно строить сложные условия для хандлеров.


Как работать с библиотекой? Легко и интуитивно понятно! Для начала нужно импортировать саму библиотеку и создать бота:
```python
from asyncVK import Handler, Bot, run_polling
from asyncVK.dispatcher import Dispatcher
from asyncVK.condition import Condition, And, Or
import asyncVK.keyboard as keyboard


TOKEN = "access_token"
GROUP_ID = 182801600

bot = Bot(TOKEN, GROUP_ID)
```


Теперь мы можем запустить бота на `LongPoll API`:
```python
if __name__ == "__main__":
    run_polling(bot)
```


Сейчас бот запущен, но ни на что не реагирует. Чтобы это исправить нам нужно создать обработчик и добавить его в бота. Как это сделать? Вот так:
```python
@bot.handle
@Handler.on.message_new(Condition(command="привет!"), is_lower=True)
async def handler(dispatcher: Dispatcher): 
    await dispatcher.send_message("Hi!")
```


В примере выше мы создали обработчик новых сообщений с помощью декоратора ```python @Handler.on.message_new``` и добавили его в бота с помощью декоратора ```python @bot.handle```
