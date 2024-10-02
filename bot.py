from telegram.ext import ApplicationBuilder, MessageHandler, filters, CallbackQueryHandler, CommandHandler

from gpt import *
from util import *

async def start(update, context):
    dialog.mode = 'main'
    text = load_message('main')
    await send_photo(update, context, 'main')
    await send_text(update, context, text)

    await show_main_menu(update, context, {
        'start': 'Start',
        'profile': 'Profile',
        'opener': 'Opener',
        'message': 'Message',
        'date': 'Date',
        'gpt': 'GPT Chat',
    })

async def gpt(update, context):
    dialog.mode = 'gpt'
    text = load_message('gpt')
    await send_photo(update, context, 'gpt')
    await send_text(update, context, text)

async def gpt_dialog(update, context):
    text = update.message.text
    prompt = load_prompt('gpt')
    answer = await chatgpt.send_question(prompt, text)
    await send_text(update, context, answer)

async def date(update, context):
    dialog.mode = 'date'
    text = load_message('date')
    await send_photo(update, context, 'date')
    await send_text_buttons(update, context, text, {
        'date_grande': 'Ariana Grande',
        'date_robbie': 'Margo Robby',
        'date_zendaya': 'Zendeya',
        'date_gosling': 'Ryan Gosling',
        'date_hardy': 'Tom Hardi',
    })

async def date_dialog(update, context):
    text = update.message.text
    my_message = await send_text(update, context, 'The person is typing you, wait...')
    answer = await chatgpt.add_message(text)
    await my_message.edit_text(answer)

async def date_button(update, context):
    query = update.callback_query.data
    await update.callback_query.answer()

    await  send_photo(update, context, query)
    await send_text(update, context, 'Noice choice')

    prompt = load_prompt(query)
    chatgpt.set_prompt(prompt)

async def message(update, context):
    dialog.mode = 'message'
    text = load_message('message')
    await send_photo(update, context, 'message')
    await send_text_buttons(update, context, text, {
        'message_next': 'Next message',
        'message_date': 'Invite to date',
    })
    dialog.list.clear()

async  def message_button(update, context):
    query = update.callback_query.data
    await update.callback_query.answer()

    prompt = load_prompt(query)
    user_chat_history = '\n\n'.join(dialog.list)
    my_message = await send_text(update, context, 'GPT rendering request, wait...')
    answer = await chatgpt.send_question(prompt, user_chat_history)
    await my_message.edit_text(answer)

async  def message_dialog(update, context):
    text = update.message.text
    dialog.list.append(text)

async def profile(update, context):
    dialog.mode = 'profile'
    text = load_message('profile')
    await send_photo(update, context, 'profile')
    await  send_text(update, context, text)

    dialog.user.clear()
    dialog.count = 0
    await send_text(update, context, 'How old are you?')

async def profile_dialog(update, context):
    text = update.message.text
    dialog.count += 1

    if dialog.count == 1:
        dialog.user['age'] = text
        await send_text(update, context, 'What is your job duty?')
    elif dialog.count == 2:
        dialog.user['occupation'] = text
        await send_text(update, context, 'Do you have a hobby?')
    elif dialog.count == 3:
        dialog.user['hobby'] = text
        await send_text(update, context, 'What did you dislike?')
    elif dialog.count == 4:
        dialog.user['annoys'] = text
        await send_text(update, context, 'What is purpose of dating?')
    elif dialog.count == 5:
        dialog.user['goals'] = text
        prompt = load_prompt('profile')
        user_info = dialog_user_info_to_str(dialog.user)

        my_message = await send_text(update, context, 'GPT generating your profile, wait please...')
        answer = await  chatgpt.send_question(prompt, user_info)
        await my_message.edit_text(answer)

async def opener(update, context):
    dialog.mode = 'opener'
    text = load_message('opener')
    await send_photo(update, context, 'opener')
    await  send_text(update, context, text)

    dialog.user.clear()
    dialog.count = 0
    await send_text(update, context, 'What is a girl name?')

async def opener_dialog(update, context):
    text = update.message.text
    dialog.count += 1

    if dialog.count == 1:
        dialog.user['name'] = text
        await send_text(update, context, 'How old is she?')
    elif dialog.count == 2:
        dialog.user['age'] = text
        await send_text(update, context, 'How beatiful is she from 1 to 10?')
    elif dialog.count == 3:
        dialog.user['handsome'] = text
        await send_text(update, context, 'What is she is doing for her living?')
    elif dialog.count == 4:
        dialog.user['occupation'] = text
        await send_text(update, context, 'What is purpose of dating?')
    elif dialog.count == 5:
        dialog.user['goals'] = text
        prompt = load_prompt('opener')
        user_info = dialog_user_info_to_str(dialog.user)

        answer = await  chatgpt.send_question(prompt, user_info)
        await send_text(update, context, answer)

async def hello(update, context):
    if dialog.mode == 'gpt':
        await gpt_dialog(update, context)
    if dialog.mode == 'date':
        await date_dialog(update, context)
    if dialog.mode == 'message':
        await message_dialog(update, context)
    if dialog.mode == 'profile':
        await profile_dialog(update, context)
    if dialog.mode == 'opener':
        await opener_dialog(update, context)
    else:
        await send_text(update, context, '*Hello*')
        await send_text(update, context, '_How are you?_')
        await send_text(update, context, 'You wrote ' + update.message.text)
        await send_photo(update, context, 'avatar_main')
        await send_text_buttons(update, context, 'Start flow? ', {
            'start': 'Start',
            'stop': 'Stop',
        })

async def hello_button(update, context):
    query = update.callback_query.data
    if query == 'start':
        await send_text(update, context, 'The proccesse initiated')
    else:
        await send_text(update, context, 'The proccesse is already started')


dialog = Dialog()
dialog.mode = None
dialog.list = []
dialog.count = 0
dialog.user = {}

chatgpt = ChatGptService(token='gpt:1EprHW2fyrbq2MNxmQbRJFkblB3TJuC8zKn6VeGdT0tnEKbw')

app = ApplicationBuilder().token("7622784824:AAHAFDmvkLEaWxWW3sEjpfHxJVVNsKT7VnQ").build()
app.add_handler(CommandHandler('start', start))
app.add_handler(CommandHandler('gpt', gpt))
app.add_handler(CommandHandler('date', date))
app.add_handler(CommandHandler('message', message))
app.add_handler(CommandHandler('profile', profile))
app.add_handler(CommandHandler('opener', opener))

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, hello))

app.add_handler(CallbackQueryHandler(date_button, pattern="^date_.*"))
app.add_handler(CallbackQueryHandler(message_button, pattern="^message_.*"))
app.add_handler(CallbackQueryHandler(hello_button))
app.run_polling()
