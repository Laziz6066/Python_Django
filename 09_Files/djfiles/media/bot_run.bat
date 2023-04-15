@echo off

call %~dp0Youtube_bot/venv/Scripts/activate

cd %~dp0Youtube_bot

set TOKEN=5666638569:AAHMLrGg9IBpgf8u1wMkd_35eBiMsmpqDMI

python bot_telegram.py

pause