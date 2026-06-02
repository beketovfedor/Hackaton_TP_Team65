#!/usr/bin/env bash

set -e

echo "===================================="
echo " Запуск сортировщика писем"
echo "===================================="

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
LOG_DIR="$PROJECT_DIR/logs"
LOG_FILE="$LOG_DIR/app.log"

echo "Проект: $PROJECT_DIR"

mkdir -p "$LOG_DIR"

if [ ! -d "$PROJECT_DIR/src" ]; then
    echo "Ошибка: папка src не найдена"
    exit 1
fi

if [ ! -d "$PROJECT_DIR/data" ]; then
    echo "Ошибка: папка data не найдена"
    exit 1
fi

if [ ! -d "$PROJECT_DIR/data/inbox" ]; then
    echo "Ошибка: папка data/inbox не найдена"
    exit 1
fi

if [ ! -f "$PROJECT_DIR/data/config/categories.json" ]; then
    echo "Ошибка: файл data/config/categories.json не найден"
    exit 1
fi

mkdir -p "$PROJECT_DIR/data/processed"

if [ -f "$PROJECT_DIR/.venv/bin/python" ]; then
    PYTHON="$PROJECT_DIR/.venv/bin/python"
elif [ -f "$PROJECT_DIR/.venv/Scripts/python.exe" ]; then
    PYTHON="$PROJECT_DIR/.venv/Scripts/python.exe"
else
    PYTHON="python3"
fi

echo "Python: $PYTHON"
echo "Лог-файл: $LOG_FILE"
echo "Запуск приложения..."
echo "------------------------------------"

cd "$PROJECT_DIR"

"$PYTHON" -m src.main "$@" 2>&1 | tee "$LOG_FILE"

echo "------------------------------------"
echo "Работа приложения завершена"
echo "Лог сохранён в: $LOG_FILE"