# Подсчёт средней зарплаты по языкам программирования

Программа позволяет получить вакансии с [HeadHunter](https://hh.ru/) и [SuperJob](https://www.superjob.ru/) по профессии `Программист`

Данные собираются по след. языкам программирования:
*  Python
*  Java
*  C#

### Как установить
Для получения данных с сайта SuperJob, необходимо получить секретный ключ на https://api.superjob.ru/register и сохранить его в переменную окружения `SUPERJOB_KEY`. 

Python3 должен быть уже установлен.
Затем используйте `pip` (или `pip3`, есть конфликт с Python2) для установки зависимостей:
```console
$ pip install -r requirements.txt
```

### Как запускать
```console
$ python3 main.py
```
