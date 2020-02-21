import requests
import os
from param import token
'''
Импорт токена из файла param.py
'''
def move_to_yadisk(from_lang, to_lang):
    Y_URL = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
    path_file = os.path.join('{}-{}_translate.txt'.format(from_lang.upper(), to_lang.upper()))
    params = {
        'path': path_file
    }

    headers = {
        'Authorization': token
    }

    response = requests.get(Y_URL, params=params, headers=headers)
    new_url = response.json()['href']
    with open('{}-{}_translate.txt'.format(from_lang.upper(), to_lang.upper()), encoding='UTF-8') as f:
        response = requests.put(new_url, data=f.read().encode('UTF-8'))

def translate_it(text, from_lang, to_lang):
    API_KEY = 'trnsl.1.1.20190712T081241Z.0309348472c8719d.0efdbc7ba1c507292080e3fbffe4427f7ce9a9f0'
    URL = 'https://translate.yandex.net/api/v1.5/tr.json/translate'
    params = {
        'key': API_KEY,
        'text': text,
        'lang': '{}-{}'.format(from_lang, to_lang),
    }

    response = requests.get(URL, params=params)
    if response.json()["code"] == 501:
        return
    else:
        json_ = response.json()
        return ''.join(json_['text'])

def main():
    while True:
        next_step = input('Для перевода текста нажмите n\n'
                          'Для выхода из программы нажмие q\n')
        if next_step == 'n':
            try:
                from_lang = input('Введите с какого языка перевести текст: ')
                to_lang = input('Введите на какой язык перевести текст: ')
                with open('{}.txt'.format(from_lang.upper()), encoding='UTF-8') as translate:
                    text = translate.read().strip()
            except FileNotFoundError:
                print(f'Документа на языке {from_lang} нет')
            else:
                if translate_it(text, from_lang, to_lang) == None:
                    print('Неправильно введен язык перевода')
                else:
                    with open('{}-{}_translate.txt'.format(from_lang.upper(), to_lang.upper()), 'w', encoding='UTF-8') as translate:
                        translate.write(translate_it(text, from_lang, to_lang))
                        print('Документ успешно переведен')
                    move = input('Для передачи переведенного документа на Яндекс Диск нажмите y:\n'
                                 'Для выхода нажмите q: ')
                    if move == 'y':
                        move_to_yadisk(from_lang,to_lang)
                        print('Документ успешно добавлен на Яндекс Диск')
                    elif move == 'q':
                        break
        elif next_step == 'q':
            break
main()

