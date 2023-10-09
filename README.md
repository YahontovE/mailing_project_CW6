# Сервис рассылок

### Используемые технологии
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white) ![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white) ![Bootstrap](https://img.shields.io/badge/bootstrap-%238511FA.svg?style=for-the-badge&logo=bootstrap&logoColor=white) ![HTML](https://img.shields.io/badge/html-%23E34F26.svg?style=for-the-badge&logo=html&logoColor=white) ![CSS](https://img.shields.io/badge/css-%231572B6.svg?style=for-the-badge&logo=css&logoColor=white) ![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E) ![Redis](https://img.shields.io/badge/redis-%23DD0031.svg?style=for-the-badge&logo=redis&logoColor=white)
____

### Описание
Чтобы удержать текущих клиентов, часто используют вспомогательные, или «прогревающие», рассылки для информирования и привлечения клиентов.
В связи с этим был разработан сервис управления рассылками, администрирования и получения статистики.

____

### Как использовать данный проект?
* Склонировать репозиторий в IDE
* Установить вирутальное окружение

  В терминале ввести команду:
  ```
  python3 -m venv venv
  ```
* Активировать виртуальное окружение

  В терминале ввести команду:
  ```
  source venv/bin/activate
  ```
* Установить зависимости

  В терминале ввести команду:
  ```
  pip install -r requirements.txt
  ```
  Установить редис на ваш компьютер
* Создать файл ``.env``. Его необходимо заполнить данными из файла ``.env.sample``
* Создать базу данных, одноименную с названием базы данных в заполненном вами файле ``.env``
* Создать и применить миграции

  В терминале ввести следующие команды:
  ```
  python3 manage.py makemigrations
  ```
  ```
  python3 manage.py migrate
  ```
* Создать суперпользователя с данными, которые находятся модуле ``csu.py``
* Создать суперпользователя с данными, которые находятся модуле ``cmu.py``

  В терминале ввести команду:
  ```
  python3 manage.py csu
  ```
* Запустить сервер локально

  В терминале ввести команду:
  ```
  python3 manage.py runserver
  ```
____
### Можно пользоваться
