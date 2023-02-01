import json
import os
import re
import sys

import pandas as pd
import numpy as np

from vosk import Model, KaldiRecognizer, SetLogLevel
from pydub import AudioSegment
from text2num import word_to_nums


def check_first(check_list, for_name=False):
    value = np.NaN
    try:
        int(check_list[2])
        if not for_name:
            value = check_list[2]
    except:
        pass
    try:
        int(check_list[0])
        value = check_list[0]
    except:
        pass
    return value


def check_number(check_list, indices_list, check_first_flag=False):
    value = np.NaN if not check_first_flag else check_first(check_list)
    if indices_list:
        last_index = indices_list[-1]
        if last_index == len(check_list) - 1:
            try:
                int(check_list[last_index - 1])
                value = check_list[last_index - 1]
            except:
                pass
        else:
            try:
                int(check_list[last_index - 1])
                value = check_list[last_index - 1]
            except:
                pass
            try:
                int(check_list[last_index + 1])
                value = check_list[last_index + 1]
            except:
                pass
    return value


def text_processing(text):
    text = re.sub(r'следующ..', 'следующий', text)
    text = re.sub(r'ошибк.', 'ошибка', text)
    text = re.sub(r'ё', 'е', text)
    text = text.replace('колесную пару', 'колесная пара')
    text = text.replace('следу ', 'следующий ')
    text = text.replace('колесную пара', 'колесная пара')
    text = text.replace('конусные пары', 'колесная пара')
    text = text.replace('конусные пара', 'колесная пара')
    text = text.replace('конусная пара', 'колесная пара')
    text = text.replace('рама нам пора', 'рама боковая')
    text = text.replace('равно', 'рама')
    text = text.replace('шарам', 'рама')
    text = text.replace('орава', 'рама')
    text = text.replace('рама буквально', 'рама боковая')
    text = text.replace('нрава', 'рама')
    text = text.replace('раз', 'рама')
    text = text.replace('рам', 'рама')
    text = text.replace('рамаа', 'рама')
    text = text.replace('рамаок', 'рама')
    text = text.replace('рамапа', 'рама')
    text = text.replace('рама кова', 'рама боковая')
    text = text.replace('рама рама', 'рама')
    text = text.replace('робкого', 'рама боковая')
    text = text.replace('боковая нона', 'рама боковая')
    text = text.replace('брака', 'брак')
    text = text.replace('запись', '')
    text = text.replace('номер номер', 'номер')
    text = text.replace('завод завод', 'завод')
    text = text.replace('год год', 'год')
    text = text.replace('рамау', 'рама')
    text = text.replace('рамаы', 'рама')
    text = text.replace('раунд', 'рама')
    text = text.replace('право боковая', 'рама боковая')
    text = text.replace('о рама', 'рама боковая')
    text = text.replace('рама баклана', 'рама боковая')
    text = text.replace('широбоковая', 'рама боковая')
    text = text.replace('рама мы', 'рама боковая')
    text = text.replace('быкова', 'боковая')
    text = text.replace('бокова', 'боковая')
    text = text.replace('боковой', 'боковая')
    text = text.replace('боковаяя', 'боковая')
    text = text.replace('буквально', 'боковая')
    text = text.replace('гайка без буксы', 'гайка, без буксы')
    text = text.replace('гайка одна букса', 'гайка, одна букса')
    text = text.replace('шайба без буксы', 'шайба, без буксы')
    text = text.replace('шайба одна буксы', 'шайба, одна букса')
    text = text.replace('набоковая', 'боковая')
    text = text.replace('вслед', 'следующий')
    text = text.replace('шайбами', 'шайба')
    text = text.replace('шайбы', 'шайба')
    text = text.replace('году', 'год')
    text = text.replace('года', 'год')
    text = text.replace('начала записи ', '').replace('начало записи ', '')
    text = text.replace('зовут', 'завод')
    text = text.replace('заводу', 'завод')
    text = text.replace('заводы', 'завод')
    text_split = text.split('следующий')
    all_text = []
    all_positions = []
    for position in text_split: 
        base_dict = {'наименование': np.NaN, 'номер': np.NaN, 'год': np.NaN, 'завод': np.NaN, 'комментарий': np.NaN}
        position = position.lstrip().rstrip()
        position = word_to_nums(position)
        position_split = position.split()
        number_indices = []
        facture_indices = []
        year_indices = []
        for idx, word in enumerate(position_split):
            if word == 'номер':
                number_indices.append(idx)
            elif word == 'завод':
                facture_indices.append(idx)
            elif word == 'год':
                year_indices.append(idx)
        if not (number_indices or facture_indices or year_indices):
            continue
        base_dict['номер'] = check_number(position_split, number_indices, check_first_flag=True)
        base_dict['завод'] = check_number(position_split, facture_indices)
        base_dict['год'] = check_number(position_split, year_indices)
        if number_indices and number_indices[0] <= 2:
            base_dict['наименование'] = ' '.join(position_split[:number_indices[0]])
        elif not isinstance(check_first(position_split, for_name=True), str):
            base_dict['наименование'] = ' '.join(position_split[:2])
        if len(str(base_dict['наименование'])) <= 6:
            base_dict['наименование'] = np.NaN
        if 'китай' in position_split:
            base_dict['завод'] = 'китай'
        if 'брак' in position_split:
            base_dict['комментарий'] = 'брак'
        elif 'шайба, без буксы' in position:
            base_dict['комментарий'] = 'шайба, без буксы'
        elif 'шайба, одна букса' in position:
            base_dict['комментарий'] = 'шайба, одна букса'
        elif 'гайка, одна букса' in position:
            base_dict['комментарий'] = 'гайка, одна букса'
        elif 'гайка, без буксы' in position:
            base_dict['комментарий'] = 'гайка, без буксы'
        elif 'одна букса' in position:
            base_dict['комментарий'] = 'одна букса'
        elif 'шайба' in position_split:
            base_dict['комментарий'] = 'шайба'
        elif 'гайка' in position_split:
            base_dict['комментарий'] = 'гайка'
        if len(str(base_dict['завод'])) > 4 and base_dict['завод'] != 'китай':
            base_dict['завод'] = base_dict['завод'][-2:]
        if len(str(base_dict['год'])) > 4:
            base_dict['год'] = base_dict['год'][:2]
        if len(str(base_dict['номер'])) > 6:
            if '20' in base_dict['номер']:
                base_dict['год'] = base_dict['номер'][5:]
                base_dict['номер'] = base_dict['номер'][:5]
            else:
                base_dict['номер'] = base_dict['номер'][:4]
#        base_dict['текст'] = position
        all_positions.append(base_dict)
        all_text.append(position)
    return pd.DataFrame(all_positions)


def df_processing(row):
    try:
        if 9 < int(row['год']) < 22:
            row['год'] = '20' + str(row['год'])
        if int(row['год']) <= 9:
            row['год'] = '200' + str(row['год'])
        elif 22 < int(row['год']) < 100:
            row['год'] = '19' + str(row['год'])
    except:
        row['год'] = np.NaN
    return row

def audio_handler(file_in, file_out, mode):
    
    SetLogLevel(0)

    # Проверяем наличие модели
    if not os.path.exists("light_model"):
        print ("Please download the model from https://alphacephei.com/vosk/models and unpack as 'model' in the current folder.")
        exit(1)

    # Устанавливаем Frame Rate
    FRAME_RATE = 16000
    CHANNELS = 1

    # загружаем модель
    model = Model("light_model")
    rec = KaldiRecognizer(model, FRAME_RATE)
    rec.SetWords(True)

    
    path = file_in
    
    if mode != 'test' and mode != 'product':
        print('Режим некорректен. Допустимые режимы: test, product')
        exit(1)
    else:
        print("Аргументы не заданы. Нужны: \n1. Путь до аудиофайла\n2. Значение test (для тестирования) / product (для работы)")
        exit(1)
    
    # загружаем аудио
    print('_______LOG_______')
    print(f'Установлен режим {mode}')
    print(f'Загружаем аудиофайл {path}', end=' - ')
    try:
        audio = AudioSegment.from_wav(path)
    except:
        print('\nПуть некорректен')
        exit(1)
        
    audio = audio.set_channels(CHANNELS)
    audio = audio.set_frame_rate(FRAME_RATE)
    print('готово')
    print(f'Преобразуем аудио в текст', end=' - ')
    rec.AcceptWaveform(audio.raw_data)
    
    all_text = json.loads(rec.FinalResult())['text']
    print('готово')
    print(f'Обрабатываем текст', end=' - ')
    final_data = text_processing(all_text)

    final_data['наименование'] = final_data['наименование'].fillna(method='ffill')
    final_data['год'] = final_data['год'].astype('float')

    final_data = final_data.apply(df_processing, axis=1)
    print('готово')
    print(f'Выгружаем данные', end=' - ')
    if mode == 'product':
        final_data.to_csv(file_out, index=False)
        print('готово')
        print(f'Файл сохранен в {file_out}')
    elif mode == 'test':
        submission = pd.read_csv('sub_example_audio.csv')
        if final_data.shape[0] <= submission.shape[0]:
            submission.iloc[:final_data.shape[0]] = final_data
            submission.to_csv(file_out, index=False)
            print('готово')
            print('Тестовый файл сохранен в result.csv')
        else:
            print(f'\nПроблема с размерностью: обработанные данные больше:{final_data.shape[0]} > {submission.shape[0]}')


if __name__ == '__main__':

    SetLogLevel(0)

    # Проверяем наличие модели
    if not os.path.exists("light_model"):
        print ("Please download the model from https://alphacephei.com/vosk/models and unpack as 'model' in the current folder.")
        exit(1)

    # Устанавливаем Frame Rate
    FRAME_RATE = 16000
    CHANNELS = 1

    # загружаем модель
    model = Model("light_model")
    rec = KaldiRecognizer(model, FRAME_RATE)
    rec.SetWords(True)

    if len(sys.argv) == 3:
        path = sys.argv[1]
        mode = sys.argv[2]
        if mode != 'test' and mode != 'product':
            print('Режим некорректен. Допустимые режимы: test, product')
            exit(1)
    else:
        print("Аргументы не заданы. Нужны: \n1. Путь до аудиофайла\n2. Значение test (для тестирования) / product (для работы)")
        exit(1)
    
    # загружаем аудио
    print('_______LOG_______')
    print(f'Установлен режим {mode}')
    print(f'Загружаем аудиофайл {path}', end=' - ')
    try:
        audio = AudioSegment.from_wav(path)
    except:
        print('\nПуть некорректен')
        exit(1)
        
    audio = audio.set_channels(CHANNELS)
    audio = audio.set_frame_rate(FRAME_RATE)
    print('готово')
    print(f'Преобразуем аудио в текст', end=' - ')
    rec.AcceptWaveform(audio.raw_data)
    
    all_text = json.loads(rec.FinalResult())['text']
    print('готово')
    print(f'Обрабатываем текст', end=' - ')
    final_data = text_processing(all_text)

    final_data['наименование'] = final_data['наименование'].fillna(method='ffill')
    final_data['год'] = final_data['год'].astype('float')

    final_data = final_data.apply(df_processing, axis=1)
    print('готово')
    print(f'Выгружаем данные', end=' - ')
    if mode == 'product':
        final_data.to_csv('result.csv', index=False)
        print('готово')
        print('Файл сохранен в result.csv')
    elif mode == 'test':
        submission = pd.read_csv('sub_example_audio.csv')
        if final_data.shape[0] <= submission.shape[0]:
            submission.iloc[:final_data.shape[0]] = final_data
            submission.to_csv('result.csv', index=False)
            print('готово')
            print('Тестовый файл сохранен в result.csv')
        else:
            print(f'\nПроблема с размерностью: обработанные данные больше:{final_data.shape[0]} > {submission.shape[0]}')