# tgTaskManager
TG-Bot for tracking tasks with reminders
## Installation and configuration
1. `git clone https://github.com/GithubDenis5/tgTaskManager.git`
2. configure connection to MongpDB and RabbitMQ via _.env_ files in each service (bot_service, task_service, notification_service), examples in _.env.template_
3. `docker compose up --build`
## Main functionality
- Creating tasks with reminders
- Changing the name, description, date and time of the deadline and reminder
- Receiving notifications at the selected time
- Tracking the remaining time before the deadline
- Deleting a task on a specific date
- Saving tracking of sending notifications after restarting services
- Sending a reminder every day after the delay and before the status changes to completed