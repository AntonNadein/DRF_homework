# DRF_homework

## Описание:

Реализация платформы для онлайн-обучения, LMS-системы, в которой каждый желающий может размещать свои полезные
материалы или курсы.

Работа будет над SPA веб-приложением и результатом создания проекта будет бэкенд-сервер, который возвращает 
клиенту JSON-структуры.

## Установка:

* Клонируем репозиторий 
```
git@github.com:AntonNadein/DRF_homework.git
```
* Устанавливаем зависимости **pyproject.toml**
* Переименовываем файл .env.sample в .env и заполняем его своими данными
*
    * Настройки SECRET_KEY и DEBUG
    * Настройки подключения к базе данных
    * Секретный ключ сервиса STRIPE
    * Настройки почтового сервиса
    * Настройки CELERY
* Запускаем миграции командой 
```
python manage.py migrate
```

## Использование:

Запуск:
* Запуск обработчика очереди Celery (worker) для получения задач и их выполнения.
```
  celery -A config worker -l INFO
  команда для Windows 
  celery -A config worker -l INFO -P eventlet
```
* Запуск планировщика Celery beat.
```
  celery -A config beat -l info -S django
```
* Запуск Django командой 
```
python manage.py runserver
```
Работу каждого эндпоинта можно проверить с помощью Postman.

## Структура проекта:

#### Сайт состоит из двух основных приложений:

1. *materials* - приложение управления курсами и уроками. Содержит модели, сериализаторы, представления с основными CRUD
 операциями. Добавлена задача отправки сообщений по подписке, об обновлении курса.

2. *users* - приложение управления пользователями и группами. Содержит модели, сериализаторы, представления с основными 
CRUD операциями с пользователями, регистрация пользователей в проекте настроена JSON Web Token (JWT)-авторизации.
Добавлена функция оплаты курса/урока при помощи стороннего APi ресурса stripe. Добавлена задача проверки активности 
пользователей.

* *config* - настройки проекта(settings.py) и настройки маршрутов (urls.py).

## Запуск проекта с помощью Docker Compose

**Подготовка к запуску проекта:**
1. Установите Docker.
2. Установите Docker Compose.
3. Убедитесь, что Docker запущен и работает.

**Запуск проекта**
1. Клонируйте репозиторий:
```
git@github.com:AntonNadein/DRF_homework.git
```
2. Переименовываем файл .env.sample в .env и заполняем его своими данными.
3. Запустите проект, выполнив команду для запуска в фоновом режиме:
```
docker-compose up -d
```

После запуска веб-приложение будет доступно по адресу: **http://localhost:8000**

**Дополнительные команды:**
- Для просмотра запущенных контейнеров:
```
docker-compose ps
```
- Для просмотра логов всех контейнеров:
```
docker-compose logs
```
- Для остановки сервисов:
```
docker-compose down
```
## Настройка CI/CD и деплой.

## Настройка сервера и ручной деплой приложения с использованием Docker.

1. ###  ***Настройка сервера на примере операционной системы Linux Ubuntu.***
- Откройте терминал и выполните команду для обновления списка пакетов:
```
sudo apt update
```
- Обновления всех установленных пакетов до их последних версий. Эта команда может потребовать подтверждения перед
началом обновления.
```
sudo apt upgrade
```
- ***Установка Docker*** https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository
  - Добавить официальный ключ GPG Docker (Выполняйте построчно): 
```
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc
```
- Добавьте репозиторий в источники Apt (Эта команда может потребовать подтверждения):
```

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
```
- Установка Docker последней версии.
```
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```
- Проверка выполнения установки.
```
sudo docker run hello-world
```
- В ответе вы должны получить *Hello from Docker!*
- ***Настройка файрвола***
- Сначала проверьте состояние файрвола с помощью команды
```
sudo ufw status
```
- Если файрвол отключен, активируйте его
```
sudo ufw enable
```
- Теперь откройте необходимые порты
- Порт 80 для HTTP:
```
sudo ufw allow 80/tcp
```
- Порт 443 для HTTPS:
```
sudo ufw allow 443/tcp
```
- Порт Порт 22 нужен для работы протокола Secure Shell (SSH):
```
sudo ufw allow 22/tcp
```
- Проверьте настройки файрвола, чтобы убедиться, что правила применились (порты 80,443 и 22 находятся в состоянии 
ALLOW).
```
sudo ufw status
```
2. ### ***Ручной деплой приложения с использованием Docker.***
- Перейдите в директорию, где вы хотите разместить код вашего приложения.
- Затем выполните команду для клонирования репозитория (если вы клонируете главную ветку main):
```
https://github.com/AntonNadein/DRF_homework.git
```
- Если вы клонируете НЕ главную ветку. В этом случае будут загружены все ветки репозитория, но проверка будет 
выполнена в указанной, и эта ветка станет настроенной локальной веткой:
```
git clone --branch <имя_ветки> https://github.com/AntonNadein/DRF_homework.git
```
- Добавьте переменные окружения для данного репозитория.
```
cd DRF_homework
```
```
nano .env
```
***Данные требующиеся для запуска приложения***
```
SECRET_KEY=

DEBUG=

POSTGRES_DB=
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_HOST=
PORT=
POSGTRES_USER=

STRIPE_SECRET_KEY=

EMAIL_HOST=
EMAIL_PORT=
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
EMAIL_USE_TLS=
EMAIL_USE_SSL=

CELERY_BROKER_URL=
CELERY_BROKER_BACKEND=
```
- Выполните команду для запуска контейнеров.
```
docker-compose up -d
```
- Остановка контейнеров.
```
docker-compose stop
```
- Удаление контейнеров.
```
docker-compose down
```
**Возможные проблемы:**
- Добавить текущего пользователя, который вошёл в систему, в группу Docker. Если нужно добавить другого пользователя,
то значение $USER следует заменить на желаемое имя пользователя
```
sudo usermod -aG docker $USER
```
-  Установить Docker Compose из репозитория Ubuntu.
```
sudo apt install docker-compose
```

3. ### ***Настройка GitHub Actions***

1) **Клонируйте репозиторий непосредственно на локальную машину для внесения изменений в проект.**
```
git clone https://github.com/AntonNadein/DRF_homework.git
```

2) **Добавьте секретные данные**
- В данном репозитории GitHub перейдите по пути **Settings > Secrets and variables > Actions**.
- Добавьте секретные переменные:
```
ENV → Переменные окружения(указаны в пункте выше:"Данные требующиеся для запуска приложения")
DOCKER_HUB_USERNAME → Ваш login в DOCKER
DOCKER_ACCESS_TOKEN → Docker Hub token https://app.docker.com/settings/personal-access-tokens
SSH_KEY → Серверный закрытый SSH-ключ 
SSH_USER → login сервера (например: admin)
SERVER_IP → IP сервера (например: 192.168.1.1)
REPO_NAME → Имя репозитория (например: DRF_homework)
```
3) **Workflow:**
- Автоматически запускается
- Этапы workflow:
	- ✅ lint→ ✅ tests → ✅ build → 🚀 deploy

## API Документация:
* http://127.0.0.1:8000/redoc/
* http://${{ secrets.SERVER_IP }}/redoc/

## Лицензия:
Этот проект не имеет лицензий.