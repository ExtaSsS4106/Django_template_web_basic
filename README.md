# Django Template Web Basic

[![docs](https://img.shields.io/badge/docs-online-brightgreen)](https://extasss4106.github.io/Django_template_web_basic/)
[![GitHub](https://img.shields.io/badge/github-repo-blue?logo=github)](https://github.com/ExtaSsS4106/Django_template_web_basic)

Документация к базовому проекту на Django 6.1.1. Проект представляет собой серверный веб-сайт с HTML-шаблонами, регистрацией пользователей, входом через сессии Django и профилем пользователя с необязательным аватаром.

> Этот репозиторий не содержит Django REST Framework, JWT-аутентификацию или JSON API. Описание ниже соответствует текущему коду проекта.

## Назначение

Шаблон предназначен для быстрого старта небольшого Django-приложения с:

- домашней страницей на базе наследуемых шаблонов;
- регистрацией пользователя через `UserCreationForm`;
- входом и выходом с использованием стандартной сессионной авторизации Django;
- обязательным email при регистрации;
- автоматически создаваемым профилем `Profiles`;
- необязательным файлом аватара;
- административной панелью Django;
- SQLite-базой данных для локальной разработки.

## Требования

- Python 3.12 или совместимая версия;
- `pip`;
- Django 6.1.1;
- SQLite, поставляемый с Python.

## Установка и запуск

Команды выполняются из корня проекта:

```bash
python -m venv venv
source venv/bin/activate          # Linux/macOS
# venv\\Scripts\\activate       # Windows

pip install -r req.txt
python manage.py migrate
python manage.py check
python manage.py runserver
```

После запуска сайт доступен по адресу `http://127.0.0.1:8000/`.

Запуск на другом порту или с доступом из локальной сети:

```bash
python manage.py runserver 0.0.0.0:8010
```

Создание администратора:

```bash
python manage.py createsuperuser
```

Административная панель: `http://127.0.0.1:8000/admin/`.

## Зависимости

Файл зависимостей называется `req.txt`. В текущей конфигурации в нём указаны:

```text
asgiref==3.12.1
Django==6.1.1
mysqlclient==2.2.7
```

Приложение по умолчанию использует SQLite, поэтому `mysqlclient` нужен только при планировании подключения MySQL и может потребовать системные пакеты разработчика.

## Маршруты

Корневой файл `src/urls.py` подключает административную панель, маршруты `mainapp` и стандартные маршруты авторизации Django.

| Метод | URL | Назначение | Требуется вход |
| --- | --- | --- | --- |
| `GET` | `/` | Домашняя страница `main/main.html` | Нет |
| `GET`, `POST` | `/sign-up/` | Регистрация нового пользователя | Нет |
| `GET`, `POST` | `/login/` | Стандартный `LoginView` Django | Нет |
| `GET`, `POST` | `/login_/` | Дополнительный пользовательский `login_view` | Нет |
| `GET` | `/logout/` | Выход через `django.contrib.auth.logout` | Да |
| `GET` | `/admin/` | Административная панель | Да, staff |

Стандартные auth-маршруты подключены строкой `path('', include('django.contrib.auth.urls'))`, поэтому URL `/login/` и имя маршрута `login` предоставляются самим Django. Дополнительный `/login_/` использует функцию `mainapp.views.login_view`.

## Регистрация

Страница регистрации: `GET /sign-up/`.

Форма отправляется методом `POST` на тот же URL. Поля:

- `username` — уникальное имя пользователя;
- `email` — обязательный email;
- `password1` — пароль;
- `password2` — подтверждение пароля.

`RegisterForm` наследуется от `django.contrib.auth.forms.UserCreationForm`, поэтому проверяет совпадение паролей, уникальность имени и стандартные валидаторы паролей из `AUTH_PASSWORD_VALIDATORS`.

После успешной регистрации:

1. создаётся пользователь стандартной модели Django `User`;
2. сохраняется переданный email;
3. через `Profiles.objects.update_or_create(user=user)` создаётся профиль;
4. пользователь автоматически входит в систему;
5. выполняется перенаправление на `/`.

Каждая POST-форма должна содержать CSRF-токен:

```django
{% csrf_token %}
```

## Вход и выход

Основной вход выполняется через стандартный `LoginView` Django по адресу `/login/`. Шаблон страницы — `templates/registration/login.html`. Он принимает поля `username` и `password`, проверяет учётные данные и создаёт сессию.

В проекте также оставлен альтернативный обработчик `/login_/`. Он вручную вызывает `authenticate`, показывает сообщение `Неверный логин или пароль` при ошибке и перенаправляет успешного пользователя на маршрут `index`.

Выход выполняется запросом `GET /logout/`. Представление требует авторизацию с декоратором `login_required`, удаляет текущую сессию через `auth_logout` и перенаправляет пользователя к маршруту с именем `login`. В проекте это стандартный URL `/login/`.

## Модель данных

Проект использует стандартную модель `django.contrib.auth.models.User` и собственную модель `Profiles`:

```text
Profiles
  id      BigAutoField, первичный ключ
  user    OneToOneField(User, related_name='profile', CASCADE)
  avatar  FileField, upload_to='avatars/', допускает NULL
```

Профиль доступен из пользователя как `user.profile`. При удалении пользователя его профиль удаляется каскадно.

Пример получения профиля в коде:

```python
profile = request.user.profile
```

В текущем интерфейсе поле `avatar` не выводится и не обрабатывается регистрационной формой. Чтобы загружать аватар, нужно добавить `enctype="multipart/form-data"`, поле `avatar` во view/form и настроить `MEDIA_ROOT`/`MEDIA_URL`.

## Структура проекта

```text
.
├── manage.py                 # CLI Django
├── req.txt                   # зависимости Python
├── db.sqlite3                # локальная база данных
├── src/
│   ├── settings.py           # настройки проекта
│   ├── urls.py               # корневые маршруты
│   ├── asgi.py               # ASGI-точка входа
│   └── wsgi.py               # WSGI-точка входа
├── mainapp/
│   ├── views.py              # домашняя страница, auth и регистрация
│   ├── forms.py              # RegisterForm
│   ├── models.py             # модель Profiles
│   ├── urls.py               # маршруты приложения
│   ├── admin.py              # конфигурация админки
│   ├── tests.py              # место для тестов
│   └── migrations/           # миграции базы данных
├── templates/
│   ├── main/                 # базовый и домашний шаблоны
│   └── registration/         # страницы входа и регистрации
└── DOCS/                     # документация проекта
```

## Шаблоны и интерфейс

- `templates/main/index.html` содержит основную HTML-оболочку и подключает Bootstrap 5.3.8 с CDN.
- `templates/main/main.html` наследует `main/index.html` и оставляет блок `content` для содержимого главной страницы.
- `templates/registration/login.html` содержит форму входа.
- `templates/registration/reg.html` содержит форму регистрации.

Главная оболочка отображает разные пункты навигации в зависимости от `user.username`. В ней также есть ссылки на разделы `profile` и `my_sessions`, но соответствующих маршрутов в текущем `mainapp/urls.py` нет. Эти ссылки необходимо добавить или удалить при развитии проекта.

## Работа с миграциями

После изменения моделей:

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py showmigrations
```

Миграция `0001_initial.py` создала старые модели `Staff`, `Users`, `StaffInfo` и `Sessions`. Миграция `0002_...` удаляет их и добавляет актуальную модель `Profiles`, связанную со стандартным `User`. Существующую историю миграций не следует переписывать в общем репозитории без отдельной процедуры миграции данных.

## Настройки

Основные настройки находятся в `src/settings.py`:

- `DEBUG = True`;
- `ALLOWED_HOSTS = ['*']`;
- `SECRET_KEY` прописан непосредственно в файле;
- база данных — SQLite в `db.sqlite3`;
- язык — `en-us`;
- часовой пояс — `UTC`;
- шаблоны ищутся в каталоге `templates/`;
- `LOGIN_URL = '/login/'`;
- `LOGIN_REDIRECT_URL = '/'`.

В текущем файле настроен `MAILERS` с консольным backend. Для отправки настоящих писем требуется перейти на поддерживаемую конфигурацию email backend Django и задать параметры через переменные окружения.

## Проверка и тесты

Полезные команды:

```bash
python manage.py check
python manage.py test
python manage.py shell
```

`mainapp/tests.py` пока содержит только заготовку `TestCase`. Перед использованием проекта рекомендуется добавить тесты для:

- успешной и неуспешной регистрации;
- обязательности email и проверки паролей;
- входа и выхода;
- создания профиля после регистрации;
- доступа к страницам для анонимных и авторизованных пользователей;
- корректности всех ссылок главной страницы.

## Известные ограничения

1. **Секреты в настройках.** `SECRET_KEY` находится в исходном коде.
2. **Development-настройки.** `DEBUG = True` и `ALLOWED_HOSTS = ['*']` нельзя использовать в production.
3. **Нет media-настроек.** Модель содержит `FileField`, но `MEDIA_ROOT`, `MEDIA_URL` и раздача media-файлов не настроены.
4. **Лишние ссылки.** В навигации есть `profile` и `my_sessions`, но маршруты отсутствуют.
5. **Пустая главная страница.** `main/main.html` пока не добавляет контент в блок `content`.
6. **Нет тестов.** Автоматическая проверка бизнес-логики ещё не реализована.
7. **Дублирование входа.** Одновременно доступны стандартный `/login/` и альтернативный `/login_/`; желательно оставить один согласованный сценарий.
8. **Bootstrap через CDN.** Для автономной или закрытой среды зависимости фронтенда следует обслуживать локально.

## Подготовка к production

- перенесите `SECRET_KEY` в переменную окружения;
- установите `DEBUG = False`;
- задайте конкретные домены в `ALLOWED_HOSTS`;
- настройте HTTPS, secure cookies и CSRF trusted origins;
- настройте production WSGI/ASGI-сервер;
- добавьте `STATIC_ROOT` и выполните `collectstatic`;
- настройте `MEDIA_ROOT` и безопасную обработку загрузок;
- замените SQLite на управляемую production-базу при необходимости;
- ограничьте доступ к `/admin/`;
- добавьте тесты, логирование и резервное копирование базы.

## Полезные команды

```bash
python manage.py check
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
python manage.py test
python manage.py showmigrations
python manage.py shell
```
