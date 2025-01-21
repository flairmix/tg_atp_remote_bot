# Telegram Bot для управления статусами пользователей

Этот бот предназначен для управления статусами пользователей в Telegram. Он предоставляет пользователям возможность выбирать различные статусы ("Remote", "Sick", "Vacation"), вводить свои имена и указывать причину выбранного статуса. Бот сохраняет данные в базе данных и позволяет администратору отслеживать изменения статусов.

## Оглавление

- [Telegram Bot для управления статусами пользователей](#telegram-bot-для-управления-статусами-пользователей)
  - [Оглавление](#оглавление)
  - [Установка](#установка)
  - [Использование](#использование)
    - [Команды](#команды)
    - [Диалоговый интерфейс](#диалоговый-интерфейс)
  - [Лицензия](#лицензия)
  - [Контактная информация](#контактная-информация)

## Установка

1. Установите `uv`:
[https://docs.astral.sh/uv/getting-started/installation/](https://docs.astral.sh/uv/getting-started/installation/)

2. Создайте `.env` файл для хранения токенов и др.закрытой информации:
   ```
   git clone https://github.com/flairmix/tg_atp_remote_bot
   ```
3. Клонируйте данный `git` репозиторий:
   ```
   git clone https://github.com/flairmix/tg_atp_remote_bot
   ```
4. Создайте виртуальное окружение с `uv` 
   и установите необходимые пакеты:
   ```bash
   uv venv
   uv pip install -r pyproject.toml
   ```
5. Запуск `docker compose` с контейнерами проекта выполняется командой: 
   ```bash
   sudo docker compose up -d
   ```

6. ### Установка portainer

    - в папке `opt` создаем `docker-compose.yml`
    ```bash
   nano docker-compose.yml
    ```

    ```yml
   services:
   twportainer:
      image: portainer/portainer-ce:latest
      container_name: twportainer
      environment:
         - TZ=Europe/Moscow
      volumes:
         - /var/run/docker.sock:/var/run/docker.sock
         - /opt/twportainer/portainer_data:/data
      ports:
         - "9443:9443"
      restart: always
    ```
    - запускаем `portainer`
    ```bash
    sudo docker compose up -d
    ``` 

    - Управлять работой контейнеров далее будет возможно через `portainer` 
    - сервис `portainer` будет доступен по адресу: 
    https://192.168.88.16:9443

7. База данных pgAdmin - http://192.168.88.16:8080/browser/
8. backend litestar API - http://192.168.88.16:8000/schema/swagger

## Использование
### Команды

- `/start`: Начало взаимодействия с ботом.
- `/get_chat_id`: Получение идентификатора текущего чата.
- `/help`: Вывод небольшой подсказки.

### Диалоговый интерфейс

После запуска команды `/start` бот предложит выбрать один из статусов. После выбора статуса необходимо ввести своё имя и указать причину выбора данного статуса. Данные будут сохранены в базе данных.

## Лицензия

Этот проект распространяется под лицензией MIT. См. файл `LICENSE` для дополнительной информации.

## Контактная информация

Если у вас возникли вопросы или предложения, пожалуйста, свяжитесь с автором проекта по адресу michail.donchenko@atp-tlp.ru.
