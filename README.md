asyncVK – асинхронный фреймворк для создания ботов ВК. Преимущества: удобство, скорость выигрываемая за счёт асинхронности.
=

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

В примере выше мы создали обработчик новых сообщений с помощью декоратора `@Handler.on.message_new` и добавили его в бота с помощью декоратора `@bot.handle`.
Вместо декоратора `@bot.handle` можно конечно прописать `bot.handle(handler)`

Как работают хандлеры (обработчики)? Когда мы засовываем экземпляр класса Bot в функцию `run_polling`, мы как бы активируем метод `bot.run_polling`. `bot.run_polling` это бесконечный цикл. В экземпляре класса Bot есть список всех хандлеров, которые мы создали и добавили в него. И когда приходит какой-то ивент (событие), то этот цикл пересылает это событие всем хандлерам. И потом если условие истинно, то активируется функция, из которой мы сделали хандлер.

Что делает эта асинхронная функция? Она на сообщение "привет!" (в любом регистре) будет отвечать в тот же чат сообщением "Hi!". Как сделать чтобы она ответила не в тот же чат, а в ЛС? Легко! Заменить 
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
Или мы хотим, чтобы бот отвечал на привет или если `peer_id` равен 2000000001. В таком случае мы пишем:
```python
Condition(command="привет", peer_id=2000000001)
```
То есть прописывая дополнительные условия в Condition, мы как бы делаем `if command == "привет" or peer_id == 2000000001`. Также можно аналогично прописать вот так:
```python
Or(Condition(command="привет"), Condition(peer_id=2000000001))
```
Но лучше так не делать, лучше подобные условия прописывать без Or.

А что если мы хотим, чтобы бот отвечал либо если ему написали "привет", либо если в сообщении есть строка "а" и написал это пользователь с id 386746383. Тоже легко! Вот так:
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
		attachment – вложение сообщения (в виде части ссылки такого рода: 
		    от ссылки https://vk.com/id386746383?z=photo386746383_457256628%2Falbum386746383_0 
		    берём только photo386746383_457256628 и передаём это в качестве аргумента). 
		keyboard – кнопки ВК.
		
    dispatcher.send_message – ответить в том же чате. Список аргументов идентичен с answer.
    dispatcher.send_comment – ответить в комментариях. Список аргументов идентичен с answer, но аргумент keyboard отсутствует.
    dispatcher.mark_as_read – пометить сообщение как "прочитанное". Никаких аргументов не принимает.
    dispatcher.set_typing_status – установить статус на набор текста / запись голосового сообщения. Принимает один аргумент: 
        typing_status. Его значение по умолчанию "typing" (набор текста). Можно изменить на "audiomessage" – запись голосового сообщения.

Как создать кнопки? Тоже несложно! Вот пример:
```python
@bot.handle
@Handler.on.message_new(Condition(contains_command="прив"), is_lower=True)
async def handler(dispatcher: Dispatcher):
    buttons = keyboard.get_keyboard([
        [
            ("yes", "positive"),
            ("no", "negative")
        ],
        [
            ("hm...", "default"),
            ("by default", "primary"),
            ("never", "negative")
        ]
    ])

    await dispatcher.send_message("Содержит сообщение прив", keyboard=buttons)
```
[Результат создания кнопок](https://sun9-26.userapi.com/impf/Y1M5ziV_GLiQxaALrdTlDkOB-Vdp0nSOKH2-gA/YT8LKOXmFkM.jpg?size=624x351&quality=96&proxy=1&sign=01e1486d2e40ac2ab494541773f16109&type=album)

По умолчанию кнопки создаются обычными и одноразовыми. Чтобы сделать их многоразовыми пропишите `one_time=False`, а если хотите сделать их инлайновыми, то пропишите `inline=True`. К примеру:
```python
buttons = keyboard.get_keyboard([
    [
        ("yes", "positive"),
        ("no", "negative")
    ],
    [
        ("hm...", "default"),
        ("by default", "primary"),
        ("never", "negative")
    ]
], inline=True)
```
Тогда эти кнопки будут в сообщении (инлайновыми).

Можно строить любые запросы, даже если этого не предполагает отсутствие метода в диспетчере:
```python
@bot.handle
@Handler.on.message_new(Condition(contains_command="прив"), is_lower=True)
async def handler(dispatcher: Dispatcher):
    result = await bot.execute("messages.send", peer_id=dispatcher.peer_id, 
                               message="okay", random_id=0)
    print(result)
```
В этом примере мы на новое сообщение, содержащее "прив" отвечаем "okay" нашим построенным запросом. `peer_id` же берём из диспетчера. Какие параметры можно высунуть из диспетчера? Можно высунуть: `token`, `user_id`, `peer_id`, `post_id` (если событие это новая запись на стене, новый комментарий на стене или в обсуждении), `owner_id` (если событие было внутри группы, то `owner_id` это id группы), `event` (объект, в котором содержится вся информация о событии) и `text` (если к примеру событие это новое сообщение, то `text` это текст сообщения, если это к примеру новый комментарий, то `text` это текст комментария и т.д.)

Если вы хотите выполнить сразу несколько запросов асинхронно, то можно просто воспользовать библиотекой `asyncio`. К примеру:
```python
@bot.handle
@Handler.on.message_new(Condition(contains_command="прив"), is_lower=True)
async def handler(dispatcher: Dispatcher):
    tasks = [asyncio.create_task(dispatcher.mark_as_read()),
             asyncio.create_task(dispatcher.set_typing_status()),
             asyncio.create_task(asyncio.sleep(9))]

    await asyncio.gather(*tasks)
    await dispatcher.send_message("okay")


@bot.handle
@Handler.on.message_new(Condition(contains_command="а"), is_lower=True)
async def handler(dispatcher: Dispatcher):
    await dispatcher.send_message("Б!")
```
Хандлер, обрабатывающий сообщение, где есть строка "прив" сперва пометит сообщение как прочитанное, потом установит статус "печатает…" и через 9 секунд отправит сообщение "okay" и всё это асинхронно. 
> P.S. хандлеры друг друга не блокируют, так что во время работы первого хандлера вы можете написать "а" и бот ответит "Б!", несмотря на работу первого хандлера.

По-мимо этого можно делать хандлеры не для условий, а для всего события целиком. Например: 
```python
@bot.handle
@Handler.on("message_new")
async def handler(dispatcher: Dispatcher):
    if dispatcher.text.lower() == "abs":
        await dispatcher.send_message("peer")
    elif dispatcher.text.lower() == "help me":
        await dispatcher.send_message("no")
```
Этот хандлер будет обрабатывать все события типа `message_new`. В данном случае он на "abs" будет отвечать "peer", а на "help me" будет отвечать "no". И также регистр сообщения не важен, ибо мы применили метод `lower`. 

Так можно делать обработчики для любых событий. К примеру обработчик для новых комментариев:
```python
@bot.handle
@Handler.on("wall_reply_new")
async def handler(dispatcher: Dispatcher):
    if dispatcher.text.lower() == "nice":
        await dispatcher.send_comment("ok")
    elif dispatcher.text.lower() == "not bad":
        await dispatcher.send_comment("no, very bad!")
```

Какой обработчик использовать? Для условий или для всего события целиком? Если вам нужно сделать обработчик для простых команд (ответить на то этим и что-то в этом роде), то лучше все эти команды прописать в обработчике события, в данном случае это будет `@Handler.on("message_new")` ведь нам нужно отвечать на сообщения. А если же команды сложные, а не простые ответы с какими-то дополнительными действиями, то лучше их прописать в обработчике условия. К примеру нам нужно, чтобы при сообщении "статистика" бот получил статистику откуда-то, рассортировал и отфильтровал её и потом отправил. Такое лучше прописывать в обработчике условия, в данном случае `@Handler.on.message_new(Condition(command="статистика"))`
Но нужно смотреть на код в целом, ибо иногда может пригодится сделать исключение и написать сложную команду в обработчик события, а простую в обработчик условия. То есть выбор должен зависеть от ситуации и структуры вашего кода.

В хандлерах и в самом боте не предусмотрена синхронизация. Поэтому если вы будете пользоваться асинхронной реализацией, к примеру какой-то базы-данных, будет состояние гонки. А пользоваться синхронными реализациями базы-данных плохая идея, это снизит скорость бота. Такая структура позволяет боту быть очень быстрым. Но в фреймворке есть реализация асинхронной базы-данных с синхронизацией, которой если вы будете правильно пользоваться, то состояния гонки не будет и бот будет оставаться таким же быстрым. Пример бота с этой реализацией бд:
```python
from asyncVK.asyncDB import SQLite
```
```python
db = SQLite("data.db")
bot = Bot(TOKEN, GROUP_ID)



async def create_db():
    async with db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS profile (
                user_id INTEGER,
                money INTEGER
            )
        """)


@bot.handle
@Handler.on("message_new")
async def handler(dispatcher: Dispatcher):
    if dispatcher.text.lower() == "create db" and dispatcher.user_id == OWNER_ID:
        await create_db()
        await dispatcher.send_message("db was created!")

    elif dispatcher.text.lower() == "register":
        async with db:
            await db.execute(f"""
                INSERT INTO profile 
                VALUES ({dispatcher.user_id}, 0)
            """)

        await dispatcher.send_message("you are was registered!")


@bot.handle
@Handler.on.message_new(Condition(command="click"), is_lower=True)
async def handler(dispatcher: Dispatcher):
    async with db:
        await db.execute(f"""
            UPDATE profile
            SET money=money+1
            WHERE user_id={dispatcher.user_id}
        """)

        state = await db.execute(f"""
            SELECT money
            FROM profile
            WHERE user_id={dispatcher.user_id}
        """)

    money = state[0][0]
    await dispatcher.send_message(f"Money: {money}")
```
`OWNER_ID` это константа, которая должна ваш ID в ВК, это условие запрещает создавать база-данных кому-либо кроме вас командой. 
Что делает `async with db`?. `async with db` ждёт пока база-данных откроется для запросов, потом закрывает базу-данных для запросов и как все ваши запросы прошли к базе, она опять открывает базу-данных для запросов. 
Метод `db.execute` отправляет ваш запрос к базе-данных.

Также можно использовать глобальные переменные с синхронизацией. Вот пример:
```python
from asyncVK.asyncDB import Variable


total_money = Variable(0)


@bot.handle
@Handler.on.message_new(Condition(command="/click"), is_lower=True)
async def handler(dispatcher: Dispatcher):
    async with total_money:
        total_money.object += 1
        await dispatcher.send_message("Все деньги мира: " + str(total_money.object))
```


Весь код целиком для старта:
```python
from asyncVK import Handler, Dispatcher, Bot, run_polling
import asyncVK.keyboard as keyboard


TOKEN = "access_token"
GROUP_ID = 182801600

bot = Bot(TOKEN, GROUP_ID)


@bot.handle
@Handler.on.message_new(Condition(contains_command="прив"), is_lower=True)
async def handler(dispatcher: Dispatcher):
    buttons = keyboard.get_keyboard([
        [
            ("yes", "positive"),
            ("no", "negative")
        ],
        [
            ("hm...", "default"),
            ("by default", "primary"),
            ("never", "negative")
        ]
    ], inline=True)

    await dispatcher.send_message("Содержит сообщение прив", keyboard=buttons)
    result = await bot.execute("messages.send", peer_id=dispatcher.peer_id, 
                               message="okay", random_id=0)
    print(result)
    
    
if __name__ == "__main__":
    run_polling(bot)
```
