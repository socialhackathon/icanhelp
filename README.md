## Описание проекта

### Проблема: 
Ресурсозатратность в процессе привлечения спонсорской помощи он-лайн.  

### Решение проблемы: 
Упрощение процесса сбора пожертвований для обеих сторон (организаций и жертвователей)  
в виде централизованного инструмента, который позволяет легко создавать, формировать и рассылать объявления о сборе средств.  
в данном примере одна из версий реализации - интерактивный бот по рассылке объявлений в специализированных каналах.  

## Запуск проекта

### ОС:
Ubuntu 16.04/Arch Linux

### Требуемые пакеты:
python3  
python3-pip  
python3-virtualenv  

### Команды запуска
```bash
virtualenv --python=python3 venv  
. venv/bin/activate  
which python | grep `pwd` || echo "Venv not active!"  
pip install -r requirements.txt  
python bot.py  
```

### Файл конфигурации
config.py  

CHANNEL_ID: канал для рассылки оповещений  
STUB_SEND_INTERVAL: интервал рассылки тестовых оповещений  
BOT_TOKEN: aвторизационный токен бота *(ключ, запушенный в этот репо отозван, нужно поменять на свой)*  
RESOURCES_DIR: имя папки с тестовыми ресурсами  

