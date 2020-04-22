# flask_event_manager

Для запуска приложения локально необходимо:
1. Скопировать репозиторий;
2. Собрать контейнеры командой docker-compose build;
3. Запустить контейнеры docker-compose up.

Приложение работает по адресу http://0.0.0.0:5000/.

Endpoints:
 - / - list of events;
 - /create_user - to create a new user;
 - /login - to login as existing user;
 - /event/id - to watch or edit event with _id=id.

Link on Heroku:
https://pacific-wave-70154.herokuapp.com/
