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

В примере выше мы создали обработчик новых сообщений с помощью декоратора `@Handler.on.message_new` и добавили его в бота с помощью декоратора `@bot.handle`
Вместо декоратора `@bot.handle` можно конечно прописать `bot.handle(handler)`

Как работают хандлеры (обработчики)? Когда мы засовываем экземпляр класса Bot в функцию `run_polling`, мы как бы активируем метод `bot.run_polling`. `bot.run_polling` это бесконечный цикл. В экземпляре класса Bot есть список всех хандлеров, которые мы создали и добавили в него. И когда приходит какой-то ивент (событие), то этот цикл пересылает это событие всем хандлерам. И потом если условие истинно, то активируется функция, из которой мы сделали хандлер.

Что делает эта асинхронная функция? Она на сообщение «привет!» (в любом регистре) будет отвечать в тот же чат сообщением «Hi!». Как сделать чтобы она ответила не в тот же чат, а в ЛС? Легко! Заменить 
```python
await dispatcher.send_message("Hi!")
```
на
```python
await dispatcher.answer("Hi!")
```

Как строить условия? Какие условия можно построить? Строить условия легко, и можно построить абсолютно любые условия! Например мы хотим, чтобы бот отвечал на привет. В таком случае мы пишем:
```python
Condition(command="привет")
```
Или мы хотим, чтобы бот отвечал на привет или если peer_id равен 2000000001. В таком случае мы пишем:
```python
Condition(command="привет", peer_id=2000000001)
```
То есть прописывая дополнительные условия в Condition, мы как бы делаем `if command == "привет" or peer_id == 2000000001`. Также можно аналогично прописать вот так:
```python
Or(Condition(command="привет"), Condition(peer_id=2000000001))
```
Но лучше так не делать, лучше подобные условия прописывать без Or.

А что если мы хотим, чтобы бот отвечал либо если ему написали «привет», либо если в сообщении есть строка «а» и написал это пользователь с id 386746383. Тоже легко! Вот так:
```python
Or(
    Condition(command="привет"),
    And(Condition(contains_command="a"), Condition(user_id=386746383))
)
```

И так, давайте разбирать как же строить так любые запросы. Если мы пропишем несколько аргументов в `Condition`, то это будет ИЛИ (or). Если же мы засунем несколько условий в `And`, то тут условие будет истинным если все условия в `And` истинны, то есть это И (and). Если же мы засунем несколько условий в `Or`, то условие будет истинным если истинно хотя бы одно условие в нём, то есть это ИЛИ (or). В `And` и `Or` можно засовывать как и `Condition`, так и другие `And` и `Or`.

Вот все аргументы Condition:

    command – проверяет на равенство текста (если сообщение, то текста сообщения и т.д.) с этим аргументом.
    contains_command – проверяет на то, есть ли строка contains_command в тексте.
    user_id – проверяет на равенство id пользователя, инициировавшего событие, и этим аргументом.
    peer_id – проверяет на равенство id чата с этим аргументом.
    post_id – проверяет на равенство id записи на стене/id записи в обсуждениях с этим аргументом.
    owner_id – проверяет на равенство id сообщества, где произошло событие (если событие было в сообществе).

Вот весь список хандлеров:

    Handler.on.message_new – новое сообщение.
    Handler.on.message_edit – редактирование сообщения.
    Handler.on.wall_reply_new – новые комментарий на стене.
    Handler.on.wall_reply_edit – редактирование комментария на стене.
    Handler.on.wall_post_new – новый пост на стене.
    Handler.on.board_post_new – новый комментарий в обсуждениях.
    Handler.on.board_post_edit – редактирование комментария в обсуждениях.
    
Списки их аргументов абсолютно идентичны.

Возможности диспетчера:

    dispatcher.answer – ответить в ЛС. Можно активировать при любом событии, отправит сообщение инициатору события. Список аргументов: 
		text – текст сообщения.
		attachment – вложение сообщения (в виде части ссылки такого рода: от ссылки https://vk.com/id386746383?z=photo386746383_457256628%2Falbum386746383_0 берём только photo386746383_457256628 и передаём это в качестве аргумента). 
		keyboard – кнопки ВК.
		
    dispatcher.send_message – ответить в том же чате. Список аргументов идентичен с answer.
    dispatcher.send_comment – ответить в комментариях. Список аргументов идентичен с answer, но аргумент keyboard отсутствует.
    dispatcher.mark_as_read – пометить сообщение как «прочитанное». Никаких аргументов не принимает.
    dispatcher.set_typing_status – установить статус на набор текста / запись голосового сообщения. Принимает один аргумент: typing_status. Его значение по умолчанию “typing” (набор текста). Можно изменить на “audiomessage” – запись голосового сообщения.
