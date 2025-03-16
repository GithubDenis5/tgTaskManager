# tgTaskManager
TG-Bot для отслеживания задач с напоминаниями 
## установка и настройка
1. `git clone https://github.com/GithubDenis5/tgTaskManager.git`
2. настроить подключение к MongpDB и RabbitMQ через _.env_ файлы в каждом сервисе(bot_service, task_service, notification_service), примеры в _.env.template_
3. `docker compose up --build`
