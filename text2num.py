def word_to_nums(text):
    """
    Функция преобразования числительных в текстовой форме в числовые значения
    """
    
    nums_dict = {
    'ноль': 0,
    'нуля': 0,
    'нулю': 0,
    'нулём': 0,
    'один': 1,
    'единица': 1,
    'одного': 1,
    'одному': 1,
    'первый': 1,
    'первая': 1,
    'два': 2,
    'двух': 2,
    'двумя': 2,
    'второй': 2,
    'второго': 2,
    'три': 3,
    'трёх': 3,
    'трех': 3,
    'трём': 3,
    'тремя': 3,
    'третий': 3,
    'третьей': 3,
    'четыре': 4,
    'четырёх': 4,
    'четырём': 4,
    'четырьмя': 4,
    'четвёртой': 4,
    'четвёртый': 4,
    'четвертый': 4,
    'четвёртая': 4,
    'четверг': 4,
    'пять': 5,
    'пяти': 5,
    'пятью': 5,
    'пятой': 5,
    'пятое': 5,
    'пятый': 5,
    'пятая': 5,    
    'шесть': 6,
    'шести': 6,
    'шестью': 6,
    'шестой': 6,
    'шестого': 6,
    'семь': 7,
    'семи': 7,
    'седьмой': 7,
    'седьмого': 7,
    'седьмое': 7,    
    'восемь': 8,
    'восеми': 8,
    'восьмью': 8,
    'восьмой': 8,
    'восьмом': 8,
    'восьмого': 8,
    'девять': 9,
    'девяти': 9,
    'девятью': 9,
    'девятой': 9,
    'девятая': 9,
    'девятый': 9,
    'девятом': 9,
    'девятую': 9,
    'детей': 9,
    'десять': 10,
    'десяти': 10,
    'десятью': 10,
    'десятое': 10,
    'десятой': 10,
    'десятую': 10,
    'десятая': 10,
    'одинадцать': 11,
    'одиннадцать': 11,
    'одиннадцатый': 11,
    'одиннадцатой': 11,
    'одиннадцатая': 11,
    'двенадцать': 12,
    'двенадцатой': 12,
    'двенадцатый': 12,
    'двенадцатая': 12,
    'тринадцать': 13,
    'тринадцатый': 13,
    'тринадцатая': 13,
    'четырнадцать': 14,
    'четырнадцатый': 14,
    'четырнадцатая': 14,
    'пятнадцать': 15,
    'пятнадцатый': 15,
    'пятнадцатая': 15,
    'шестнадцать': 16,
    'шестнадцатый': 16,
    'шестнадцатая': 16,
    'семнадцать': 17,
    'семнадцатый': 17,
    'семнадцатая': 17,
    'восемнадцать': 18,
    'восемнадцатый': 18,
    'восемнадцатая': 18,
    'девятнадцать': 19,
    'девятнадцатый': 19,
    'девятнадцатая': 19
}
    decimals_dict = {
    'двадцать': 20,
    'тридцать': 30,
    'сорок': 40,
    'пятьдесят': 50,
    'шестьдесят': 60,
    'семьдесят': 70,
    'восемьдесят': 80,
    'девяносто': 90,
    'девяностый': 90,
    'девяноста': 90}
    
    hundreds_dict = {
    'сто': 100,
    'двести': 200,
    'триста': 300,
    'четыреста': 400,
    'пятьсот': 500,
    'шестьсот': 600,
    'семьсот': 700,
    'восемьсот': 800,
    'девятьсот': 900,
    'дветысячи': 2000}
    
    text = text.replace('две тысячи', 'дветысячи')
    split_text = text.split()
    new_text = []
    counter = 0
    temp_num = []
    
    for word in split_text:
        if word in hundreds_dict.keys():
            if counter == 0:
                counter = 2
                temp_num = [hundreds_dict.get(word, word)]
            else:
                new_text.append(sum(temp_num))
                counter = 0
            continue
        elif word in decimals_dict.keys():
            if counter == 2:
                temp_num.append(decimals_dict.get(word, word))
            elif counter == 1:
                new_text.append(sum(temp_num))
                temp_num = [decimals_dict.get(word, word)]
            else:
                temp_num = [decimals_dict.get(word, word)]
            counter = 1
            continue
        elif word in nums_dict.keys():
            if counter > 0:
                temp_num.append(nums_dict.get(word, word))
                counter = 0
                new_text.append(sum(temp_num))
            else:
                new_text.append(nums_dict.get(word, word))
            temp_num = []
            continue
        
        counter = 0
        if temp_num:
            temp_num = []
        else:
            new_text.append(word)
    
    new_counter = 0
    new_num = ''
    final_text = []
    for word in new_text:
        if isinstance(word, int):
            if new_counter == 0:
                new_num = str(word)
            else:
                if str(word) not in new_num:
                    new_num += str(word)
            new_counter += 1
        else:
            if new_num:
                final_text.append(new_num)
                final_text.append(word)
            else:
                final_text.append(word)
            new_counter = 0
            new_num = ''
    if new_num:
            final_text.append(new_num)
    
    # split_text = [word_to_nums_dict.get(word, word) for word in split_text]
    return ' '.join(final_text)