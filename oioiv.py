from TGBot import TinkiVinki
import series
import json

app = TinkiVinki(use_proxy=True)
series_list = series.series.keys()
series_name = ''


@app.add_handlers(lambda x: 'message' in x)
def process_messages(update, *args, **kwargs):
    print('process message')
    update = update['message']
    if 'text' in update:
        if update['text'].startswith('/'):
            command = update['text'].strip('/')
            try:
                commands_list[command](update)
            except KeyError:
                print('Command {} not found'.format(command))
        else:
            global series_name
            if series_name != '':
                chat_id = update['chat']['id']
                try:
                    reply_text = series.get_episode(series_name, update['text'])
                except Exception as e:
                    print('Cant load episode url: {}'.format(e))
                    reply_text = 'Произошла ошибка при загрузке серии. Попробуйте ещё раз'
                app.send_message(chat_id, reply_text)
                series_name = ''

            parrot(update)
    else:
        print('Not a text message')

@app.add_handlers(lambda x: 'callback_query'in x)
def process_inline(update, *args, **kwargs):
    print('process inline')
    print(update['callback_query']['data'])


def get_series_list(update):
    buttons = []
    for s in series_list:
        buttons.append({'text': s, 'callback_data': s})
    keyboard = {'inline_keyboard':[buttons]}
    chat_id = update['chat']['id']
    reply_text = 'Выберите сериал из списка'
    #reply_text = 'I got ' + ', '.join(['/' + s for s in series_list])
    app.send_message(chat_id=chat_id,
                     reply_text=reply_text,
                     reply_markup=json.dumps(keyboard))


def parrot(update):
    chat_id = update['chat']['id']
    reply_text = 'Сам ты {}'.format(update['text'])
    app.send_message(chat_id, reply_text)


def get_episode_num(update):
    chat_id = update['chat']['id']
    reply_text = 'Enter episode num'
    global series_name
    series_name = update['text'].strip('/')
    app.send_message(chat_id, reply_text)


def get_inline(update):
    call_back_button = {'inline_keyboard':[[{'text': 'Push me', 'callback_data': 'callback_test'}]]}
    chat_id = update['chat']['id']
    app.send_message(chat_id=chat_id,
                     reply_text='some text for callback',
                     reply_markup=json.dumps(call_back_button))


# 24.10.2019  comment -->
'''
@app.set_updates('/test')
def parrot(update):
    chat_id = update['chat']['id']
    reply_text = 'Сам ты {}'.format(update['text'])
    app.send_message(chat_id, reply_text)


@app.set_updates('/series')
def get_series_list(update):
    chat_id = update['chat']['id']
    reply_text = 'I got ' + ', '.join(['/' + s for s in series_list])
    app.send_message(chat_id, reply_text)


for s in series_list:
    @app.set_updates('/' + s)
    def get_episode(update):
        series_name = update['text'].strip('/')
        chat_id = update['chat']['id']
        reply_text = ' ' + ', '.join(['/' + s for s in series_list])
'''
# 24.10.2019  comment <--


if __name__ == "__main__":
    commands_list = {'series': get_series_list}
    for s in series_list:
        commands_list[s] = get_episode_num
    commands_list['inline'] = get_inline
    print('Hello')
    app.run()
