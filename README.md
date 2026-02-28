asyncVK – асинхронный фреймворк для создания ботов ВК. Преимущества: удобство, скорость выигрываемая за счёт асинхронности.
=

Бот создаётся за счёт пяти основных структурных единиц: 
1) Bot – это самая главная структурная единица. Это собственно сам бот, который подаёт ивенты     обработчикам.
2) Handler – эта структурная единица отвечает за обработку ивентов. 
3) Dispatcher – эта структурная единица отвечает за взаимодействие с ВК (ответы на сообщения, добавление комментариев). Она автоматически настраивается хандлерами.
4) Condition (Condition, And, Or) – эта структурная единица отвечает за условия. С помощью неё можно строить сложные условия для хандлеров.
5) Chain - эта структурная единица позволяет создавать цепочки команд.

Также есть такие второстепенные структурные единицы как:
1) Keyboard – это второстепенная структурная единица. Она отвечает за создание кнопок в ВК.
2) Message - структура сообщения для облегчения работы с сообщениями.

Как работать с библиотекой? Легко и интуитивно понятно! Для начала нужно импортировать саму библиотеку и создать бота:
```python
from asyncVK import Handler, Bot, run_polling
from asyncVK.dispatcher import Dispatcher
from asyncVK.condition import Condition, And, Or


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
Стоит также заметить, что хандлер без условия будет срабатывать всегда, когда активируется нужное событие (то есть вне зависимости от условий, наверное потому что их нет) - `@Handler.on.message_new()`

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
		Возвращает структуру Message вашего сообщения.

    dispatcher.reply - ответить на сообщение пользователя. Список аргументов и возвращаемое значение идентичны с answer.
    dispatcher.send_message – ответить в том же чате. Список аргументов и возвращаемое значение идентичны с answer.
    dispatcher.send_comment – ответить в комментариях. Список аргументов идентичен с answer, но аргумент keyboard отсутствует.
    dispatcher.mark_as_read – пометить сообщение как "прочитанное". Никаких аргументов не принимает.
    dispatcher.set_typing_status – установить статус на набор текста / запись голосового сообщения. Принимает один аргумент: 
        	typing_status. Его значение по умолчанию "typing" (набор текста). Можно изменить на "audiomessage" – запись голосового сообщения.
    dispatcher.kick_user - удаляет участника из беседы
        	member_id - id участника беседы (id сообщества пишется со знаком -)
    dispatcher.edit_chat_name - изменяет название беседы
        	title - новое название беседы

Пример использования структуры Message:
```python
@bot.handle
@Handler.on.message_new(Condition(command="прив"))
async def handler(dispatcher: Dispatcher):
    message = await dispatcher.reply("Это сообщение исчезнет через 3 секунды, а твоё сообщение будет закреплено")
    await asyncio.sleep(1)
    await message.edit("Это сообщение исчезнет через 2 секунды, а твоё сообщение будет закреплено")
    await asyncio.sleep(1)
    await message.edit("Это сообщение исчезнет через 1 секунду, а твоё сообщение будет закреплено")
    await asyncio.sleep(1)
    await message.delete()
    await dispatcher.message.pin()
```

Можно строить любые запросы, даже если этого не предполагает отсутствие метода в диспетчере:
```python
@bot.handle
@Handler.on.message_new(Condition(contains_command="прив"), is_lower=True)
async def handler(dispatcher: Dispatcher):
    result = await bot.execute("messages.send", peer_id=dispatcher.peer_id, 
                               message="okay", random_id=0)
    print(result)
```
В этом примере мы на новое сообщение, содержащее "прив" отвечаем "okay" нашим построенным запросом. `peer_id` же берём из диспетчера.

Параметры диспетчера:

    dispatcher.token - ваш токен
    dispatcher.user_id - id инициировавшего событие пользователя
    dispatcher.peer_id - id чата (если это ЛС, то peer_id равен user_id)
    dispatcher.post_id - id записи на стене или обсуждения (если событие это новая запись на стене, новый комментарий на стене или в обсуждении)
    dispatcher.owner_id - если событие было внутри группы, то owner_id это id группы
    dispatcher.object_id - id объекта события
    dispatcher.event - объект события
    dispatcher.text - если к примеру событие это новое сообщение, то text это текст сообщения, если это к примеру новый комментарий, то text это текст комментария и т.д.
    dispatcher.reply_text - текст отвеченного сообщения (если таковое имеется)
    dispatcher.reply_user_id - id пользователя написавшего отмеченное сообщение (если таковое имеется)
    dispatcher.reply_peer_id - id чата отмеченного сообщения (если таковое имеется)
    dispatcher.reply_object_id - id объекта ответа
    dispatcher.action_type - тип действия
    dispatcher.action_text - текст действия
    dispatcher.action_object_id - id объекта действия
    dispatcher.action_member_id - id пользователя, инициировавшего действие
    dispatcher.payload - payload
    dispatcher.message - выдаёт структуру Message для сообщения из события
    dispatcher.reply_message - выдаёт структуру Message для отвеченного сообщения из события

Возможность структуры Message:

    message.edit - изменить сообщение
    		text - новый текст
		attachment - вложение
 		keyboard - клавиатура
    message.pin - закрепить сообщение
    message.delete - удалить сообщение

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

В хандлерах и в самом боте не предусмотрена синхронизация. Поэтому если вы будете пользоваться асинхронной реализацией, к примеру какой-то базы-данных, будет возможно состояние гонки. А пользоваться синхронными реализациями базы-данных плохая идея, это снизит скорость бота. Такая структура позволяет боту быть очень быстрым. Но в библиотеке присутствует синхронизатор, с помощью которого вы можете гарантировать, что команды исполнятся точно в таком порядке, в котором они начались. Таких синхронизаторов можно использовать несколько.
```python
from asyncVK.sync import Synchronizer
```
```python
synchronizer = Synchronizer()
bot = Bot(TOKEN, GROUP_ID)



async def create_db():
    async with synchronizer:
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
        async with synchronizer:
            await db.execute("""
                INSERT INTO profile 
                VALUES (?, 0)
            """, (dispatcher.user_id,))

        await dispatcher.send_message("you are was registered!")


@bot.handle
@Handler.on.message_new(Condition(command="click"), is_lower=True)
async def handler(dispatcher: Dispatcher):
    async with synchronizer:
        await db.execute("""
            UPDATE profile
            SET money=money+1
            WHERE user_id=(?)
        """, (dispatcher.user_id,))

        state = await db.execute("""
            SELECT money
            FROM profile
            WHERE user_id=(?)
        """, (dispatcher.user_id,))

    money = state[0][0]
    await dispatcher.send_message(f"Money: {money}")
```
`OWNER_ID` это константа, которая должна ваш ID в ВК, это условие запрещает создавать база-данных кому-либо кроме вас командой. 
Что делает `async with synchronizer`?. `async with synchronizer` блокирует выполнение других блоков кода, которые также используют синхронизатор, пока внутри него исполняется код. Как код выполнится, он открывает возможность выполнения следующему в очереди блоку кода в синхронизаторе. Синхронизатор можно использовать с чем угодно, а не только с базами-данных (ОСТОРОЖНО!!! НЕ ЗЛОУПОТРЕБЛЯЙТЕ ИМ!!!)

В фреймворке также присутствует встроенный функционал создания цепочек. Что такое цепочки? Это когда команда состоит из нескольких частей. То есть, к примеру, регистрация. Вы пишите `/регистрация` и бот далее просит вас ввести имя. И вы вводите своё имя и регистрация пройдена в 2 сообщения, то есть 2 части.

```python
from asyncVK.chain import Chain, ChainResult
```

Таким образом мы импортируем класс цепочек. Как создать цепочку? Всё просто. Вместо `bot.handle` используем `chain.add_handler`, а потом `bot.add_chain(chain)`. `chain.add_handler` принимает один аргумент - название хандлера в рамках цепочки. Цепочка - это конечный автомат.

К примеру:
```python
chain = Chain()


@chain.add_handler("1")
@Handler.on.message_new(Or(Condition(contains_command="опрос")), is_lower=True)
async def handler(dispatcher: Dispatcher):
    await dispatcher.send_message("Ты нуб?")
    return ChainResult("2")


@chain.add_handler("2")
@Handler.on.message_new()
async def handler(dispatcher: Dispatcher):
    to = "2"
    if "да" in dispatcher.text.lower():
        to = None
        await dispatcher.send_message("Я так и знал")
    else:
        await dispatcher.send_message("Не ври, ты нуб?")

    return ChainResult(to)
    
    
bot.add_chain(chain)
```

Также можно пробрасывать какие-то данные по цепочке:
```python
chain = Chain()


@chain.add_handler("1")
@Handler.on.message_new(Or(Condition(contains_command="опрос")), is_lower=True)
async def handler(dispatcher: Dispatcher):
    await dispatcher.send_message("Твой ник?")
    return ChainResult("2")


@chain.add_handler("2")
@Handler.on.message_new()
async def handler(dispatcher: Dispatcher):
    await dispatcher.send_message("Твой возраст?")
    return ChainResult("3", {"name": dispatcher.text})


@chain.add_handler("3")
@Handler.on("message_new")
async def handler(dispatcher: Dispatcher):
    await dispatcher.send_message(f"Вы, месье {dispatcher.chain_data["name"]} возрастом {dispatcher.text} лет")
```

`ChainResult` имеет два аргумента. Первый это `to` - следующий хандлер в цепочке. `to` можно направить на самого себя, тем самым зациклив цепочку до выполнения определённых условий. Если `to` равен `None`, то цепочка завершается. Второй это `data` - его вы сможете получить в вашем следующем хандлере в `dispatcher.chain_data`. Также, если ничего не возвращать, то цепочка тоже завершается.

Пример использования структуры `Message` и `ActionCondition`, бот примет закреплённое сообщение и будет его удерживать в закрепе.
`ActionCondition` это условие на действие.

Возможные значения `ActionCondition`:

	chat_pin_message - закрепление сообщения
 	chat_unpin_message - открепление сообщения
  	chat_title_update - обновление названия беседы
   	chat_photo_update - обновление аватарки беседы
    	chat_photo_remove - удаление аватарки беседы
     	chat_kick_user - удаление пользователя из чата, пользователь вышел из чата
      	chat_invite_user - добавление пользователя в чат


```python
pinned_message = {"object": None}


@bot.handle
@Handler.on.message_new(Condition(contains_command="удержи"))
async def handler(dispatcher: Dispatcher):
    pinned_message["object"] = dispatcher.reply_message
    await pinned_message["object"].pin()
    await dispatcher.send_message("ok")


@bot.handle
@Handler.on.message_new(Or(ActionCondition(action="chat_pin_message"),
                           ActionCondition(action="chat_unpin_message")))
async def handler(dispatcher: Dispatcher):
    await dispatcher.send_message("Не, не выйдет")
    await pinned_message["object"].pin()
```

Методы диспетчера `send_message`, `answer`, `reply` возвращают структуру `Message`

Пример создания кнопок, а также использования пайлоада через `functional_condition`
```python
from asyncVK.core import EventParams


def check_payload(event_params: EventParams) -> bool:
    payload = event_params["payload"]
    if payload.get("answer") == "yes":
        return True
    return False


@bot.handle
@Handler.on.message_new(Condition(contains_command="дай"))
async def handler(dispatcher: Dispatcher):
    keyboard = Keyboard(
        Line(
            Button("да", "positive", {"answer": "yes"})
        ),
        Line(
            Button("нет", "negative", {"answer": "no"}),
            Button("возможно", "default", {"answer": "maybe"})
        ), one_time=True, inline=True
    )

    await dispatcher.send_message("Не дам", keyboard=keyboard)


@bot.handle
@Handler.on.message_new(Condition(functional_condition=check_payload))
async def handler(dispatcher: Dispatcher):
    await dispatcher.send_message("Ок")
    await dispatcher.send_message(f"Ваш пайлоад: {dispatcher.payload}")
```

Также существует `PayloadCondition`, который в отличие от простого `Condition` принимает все аргументы за И, а не ИЛИ по-умолчанию.
```python
@bot.handle
@Handler.on.message_new(Condition(contains_command="дай"))
async def handler(dispatcher: Dispatcher):
    keyboard = Keyboard(
        Line(
            Button("да", "positive", {"answer": "yes", "module": "vk"})
        ),
        Line(
            Button("нет", "negative", {"answer": "no"}),
            Button("возможно", "default", {"answer": "yes"})
        ), one_time=True, inline=True
    )

    await dispatcher.send_message("Не дам", keyboard=keyboard)


@bot.handle
@Handler.on.message_new(PayloadCondition(answer="yes", module="vk"))
async def handler(dispatcher: Dispatcher):
    await dispatcher.send_message("Ок")
    await dispatcher.send_message(f"Ваш пайлоад: {dispatcher.payload}")
```

В библиотеке есть возможность создавать шаблоны сообщений для дальнейшей их рассылки
```python
@bot.handle
@Handler.on.message_new(Condition(contains_command="разошли им"), is_lower=True)
async def handler(dispatcher: Dispatcher):
    await dispatcher.reply("Окей")

    message = bot.create_message_template("Вам послание, месье", forward=dispatcher.forward)
    await message.send_to("476393332,584575899")
```
В этом коде бот перешлёт сообщение двум пользователям с соответствующими id. 
Можно отправлять сообщения по-одиночному, для этого замените на `await message.send_to(476393332)`
