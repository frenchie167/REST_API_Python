## Запуск приложения

### Предварительные требования
- Установленный Docker: [https://www.docker.com](https://www.docker.com)
- Для Windows: WSL2 (рекомендуется)

### 1. Клонирование репозитория
```bash
git clone https://github.com/ваш-пользователь/ваш-репозиторий.git
cd ваш-репозиторий
```

### 2. Сборка Docker-образа
```bash
docker build -t flask-api-app .
```

### 3. Запуск контейнеров

#### File-режим (данные из JSON-файла)
```bash
docker run -d -p 5000:5000 --name api-file flask-api-app
```

#### Random-режим (генерация случайных данных)
```bash
docker run -d -p 5001:5000 -e APP_MODE=random --name api-random flask-api-app
```

#### С постоянным хранением данных (volume)
```bash
docker volume create api-data
docker run -d -p 5002:5000 -v api-data:/app --name api-persistent flask-api-app
```

### 4. Проверка работы
- File-режим: `http://localhost:5000/users`
- Random-режим: `http://localhost:5001/users`
- С постоянным хранилищем: `http://localhost:5002/users`

## Использование API

### File-режим
```http
GET    /users          # Все пользователи
GET    /users?id=UUID  # Конкретный пользователь
POST   /users          # Создать пользователя
PUT    /users          # Обновить пользователя
DELETE /users?id=UUID  # Удалить пользователя
```

### Random-режим
```http
GET    /users          # 100 случайных пользователей
GET    /users?id=any   # Один случайный пользователь
POST   /users          # Сгенерировать случайного пользователя
PUT    /users          # Сгенерировать обновленного пользователя
DELETE /users?id=any   # "Удалить" пользователя (всегда успешно)
```

## Примеры запросов

### Создание пользователя (POST)
```json
{
  "is_active": true,
  "first_name": "Иван",
  "last_name": "Иванов",
  "email": "ivan@example.com",
  "address": "Москва, ул. Пушкина 1",
  "phone_number": "+79991234567"
}
```

### Обновление пользователя (PUT)
```json
{
  "id": "c3e6f1b5-...",
  "email": "new_email@example.com",
  "address": "Санкт-Петербург, Невский пр. 5"
}
```

## Структура данных пользователя
```json
{
  "id": "c3e6f1b5-...",
  "first_name": "Анна",
  "last_name": "Петрова",
  "email": "anna@example.com",
  "registration_date": "2023-01-15",
  "is_active": true,
  "address": "ул. Лермонтова, 15, Москва, 119991",
  "phone_number": "+79997654321"
}
```

## Режимы работы

### File-режим
- Данные загружаются из файла `users.json`
- Все изменения сохраняются в файл
- Требует предварительной генерации данных
- Данные сохраняются между запусками

### Random-режим
- Данные генерируются при каждом запросе
- Не требует файла данных
- Изменения не сохраняются
- Идеален для тестирования

## Управление Docker-контейнерами

| Команда                          | Описание                              |
|----------------------------------|---------------------------------------|
| `docker ps`                      | Список работающих контейнеров         |
| `docker stop <имя_контейнера>`   | Остановить контейнер                  |
| `docker start <имя_контейнера>`  | Запустить остановленный контейнер     |
| `docker logs <имя_контейнера>`   | Показать логи контейнера              |
| `docker exec -it <имя> bash`     | Войти в контейнер                     |
| `docker rm <имя_контейнера>`     | Удалить контейнер                     |
| `docker rmi flask-api-app`       | Удалить образ                         |
| `docker volume ls`               | Список томов                          |
| `docker volume rm api-data`      | Удалить том                           |

## Генерация тестовых данных
При сборке Docker-образа автоматически генерируется 100 тестовых пользователей. Для ручной генерации:
```bash
docker exec -it api-file python datagen.py
```

## Решение проблем

### Ошибка: "docker: error during connect..."
1. Убедитесь, что Docker Desktop запущен
2. Для Windows:
   - Проверьте включен ли WSL2
   - В Docker Desktop: Settings → General → Use WSL 2 based engine
   - Выполните: `wsl --update`
3. Перезапустите Docker Desktop

### Ошибка: "failed to read dockerfile"
1. Убедитесь, что файл называется `Dockerfile` (без расширения)
2. Проверьте, что вы в правильной директории
3. Используйте явное указание файла:
   ```bash
   docker build -f Dockerfile -t flask-api-app .
   ```

### Ошибки зависимостей
Пересоберите образ без кэша:
```bash
docker build --no-cache -t flask-api-app .
```

## Технические детали
- **Python**: 3.9
- **Flask**: 2.3.2
- **Faker**: 18.11.2
- **Порт приложения**: 5000
- **Переменная окружения**: `APP_MODE` (file/random)
- **Файл данных**: `users.json`
