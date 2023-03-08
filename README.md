# Хакатон от "Первой грузовой компании"
В репозитории находится только DS-часть.

## Статус хакатона
Завершен (десятое место)

## Описание задачи
Необходимо разработать сервис для проведения аудиоинвентаризации склада.
Пользователь в процессе инвентаризации использует диктофон для записи информации, который впоследствии нужно преобразовать в табличный вид, с возможностью скачать полученные данные в формате Excel.

## Описание данных
Аудиофайлы формата *.wav

## Описание решения
1. Пользователь загружает аудиофайл на сервис.
2. Модель распознает, обрабатывает и преобразует файл в формат *.csv.
3. Пользователь может просмотреть результат работы сервиса в веб-интерфейсе и, при необходимости, внести какие-либо изменения в таблицу и скачать файл.

## Используемые библиотеки
pandas, numpy, vosk, pydub, re