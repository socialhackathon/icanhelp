## Запуск проекта

### ОС:
Ubuntu 16.04/Arch Linux

### Требуемые пакеты:
python3  
python3-pip  
python3-virtualenv  

### Команды запуска
virtualenv --python=python3 venv  
. venv/bin/activate  
which python | grep `pwd` || echo "Venv not active!"  
pip install -r requirements.txt  
python bot.py  

