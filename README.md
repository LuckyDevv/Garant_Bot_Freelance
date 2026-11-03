# 🛡️ Garant Bot — Telegram-бот сервиса онлайн-гарантов

> Коммерческий проект: бот был заказан на фриланс-бирже для сервиса онлайн-гарантов и работал в продакшне (релизы v0.3–v0.3.1-final).

[![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)](https://python.org)
[![Library](https://img.shields.io/badge/telebot-4.24-2CA5E0?style=flat-square&logo=telegram)](https://pypi.org/project/pyTelegramBotAPI/)

## 📌 О проекте

Telegram-бот для платформы онлайн-гарантов: управление гарантами и админами,
модерация чатов, рассылки, сделки и логирование. Написан на Python
(pyTelegramBotAPI), данные — в SQLite, конфигурации — JSON.

## ✨ Возможности

**Администрирование:**
- `+гарант` / `-гарант` — управление списком гарантов (вкл. онлайн/офлайн статусы)
- `+адм` / `-адм` — роли администраторов
- `/преф` — настройка префикса команд

**Модерация чатов:**
- `/бан`, `/рбан` — бан / разбан пользователя
- `/варн`, `/рварн` — предупреждения
- `/кик`, `/мут`, `/рмут` — кик и мут в чатах
- `/линк` — закрепление ссылки

**Сервисные:**
- `/mail` — рассылка сообщений по базе
- Callback-меню: списки гарантов/админов онлайн и офлайн, пагинация
- Логирование работы + уведомления админу
- Автобэкап базы (`backuper.php`)

## 🧰 Стек

- Python 3.10+, pyTelegramBotAPI 4.24
- SQLite (профили, статусы, варны)
- JSON-конфиги через собственный ConfigController

## 🚀 Запуск

```bash
git clone https://github.com/LuckyDevv/Garant_Bot_Freelance.git
cd Garant_Bot_Freelance
pip install -r requirements.txt
# Токен бота задаётся в main.py (переменная TOKEN)
python main.py
```

## 📂 Структура

```
main.py                 # точка входа, роутинг команд
Utils/
  CommandHandler.py     # обработчики команд (админ/модерация/рассылка)
  QueryHandler.py       # callback-запросы (меню, пагинация)
  DatabaseManager.py    # работа с SQLite
  ConfigController.py   # чтение/запись JSON-конфигов
  Initializer.py        # создание служебных директорий
backuper.php            # бэкап базы данных
```

## 📜 Лицензия

Код предоставлен как портфолио. Коммерческая разработка на заказ (2024).
