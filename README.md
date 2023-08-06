# ZkBridge SecondLive minter | Dev: [@python_web3](https://t.me/python_web3)
Страница минта: \
https://zkbridge.com/sbt/SecondLive-2nd-Anniversary-Commemorative-NFT

## Установка
1. [Скачиваем](https://www.python.org/downloads/) и устанавливаем Python.  
2. [Скачиваем](https://github.com/SomeWeb3/zkbridge_secondlive_minter/archive/refs/heads/main.zip) и распаковываем проект.
3. ```pip install -r requirements.txt```

## Настройка
1. Создаём `wallets.txt` и закидываем приватники.
2. В `minter.py` в 9 строке указываем границы случайной задержки в секундах между кошельками.
3. В `minter.py` в 10 строке True или False, отвечает за случайный порядок кошельков при минте.

## Запуск
1. ```python minter.py```.
