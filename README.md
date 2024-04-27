# Обменник валют

## Описание 
Python проект с использованием crud операций через нативный http server  
В качестве бд используется PostgreSQL  
Все переменные окружения хранятся в .env

## Пример .env
- DB_NAME='название бд'
- USER='пользователь бд'
- PASSWORD='пароль для пользователя'
- HOST='хост'

## Эндпоинты
- GET /currencies (Получение списка валют)
- GET /currency/EUR (Получение конкретной валюты)
- POST /currencies (Добавление валюты)  
----
- GET /exchangeRates (Получение списка всех обменных курсов)
- POST /exchangeRates (Добавление нового обменного курса в базу)
- GET /exchangeRates/USDRUB (Получение конкретного обменного курса)
- PATCH /exchangeRates/USDRUB (Обновление существующего в базе обменного курса)
----
- GET /exchange?from=BASE_CURRENCY_CODE&to=TARGET_CURRENCY_CODE&amount=$AMOUNT (Расчёт перевода определённого количества средств из одной валюты в другую)
1. В таблице ExchangeRates существует валютная пара AB - берём её курс
2. В таблице ExchangeRates существует валютная пара BA - берем её курс, и считаем обратный, чтобы получить AB
3. В таблице ExchangeRates существуют валютные пары USD-A и USD-B - вычисляем из этих курсов курс AB


TODO:
- GET /exchange?from=usd&to=eur&amount=10
- Обработать ошибки