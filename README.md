
* Клонируем проект
* Поднимаем MongoDM в докере
```bash
sudo docker-compose up -d
```
* Создаем виртуальное окружение 
```bash
python -m venv venv
```
Активируем виртуальное окружение
```bash
source venv/bin/activate
```
Устанавливаем зависимости из requirements.txt
```bash
pip install -r requirements.txt
```
Устанавливаем переменные окружения
```bash
export FLASK_APP=wsgi.py
```
* Загружаем tor браузер https://www.torproject.org/download/
* Запускаем tor браузер
* Загружаем geckodriver https://github.com/mozilla/geckodriver/releases
* В config переменной firefox_path присваиваем путь до gekodriver
* Запускаем приложение командой flask run
