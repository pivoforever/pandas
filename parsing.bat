@echo off
chcp 65001
title Запуск с виртуальным окружением

set PROJECT_PATH=%~dp0
set VENV_DIR=%PROJECT_PATH%.venv

echo Проект: %PROJECT_PATH%

:: Проверяем существование виртуального окружения
if not exist "%VENV_DIR%" (
    echo Создание виртуального окружения...
    python -m venv "%VENV_DIR%"
)

:: Активируем виртуальное окружение
call "%VENV_DIR%\Scripts\activate.bat"

:: Устанавливаем зависимости
@REM if exist "requirements.txt" (
@REM     echo Установка зависимостей из requirements.txt...
@REM     pip install -r requirements.txt
@REM ) else (
@REM     echo Установка основных библиотек...
@REM     pip install pandas requests beautifulsoup4
@REM )

echo Запуск скрипта...
python main.py

:: Деактивируем окружение (опционально)
call deactivate

pause