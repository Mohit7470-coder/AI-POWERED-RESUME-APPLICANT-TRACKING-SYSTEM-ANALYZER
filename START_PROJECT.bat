@echo off
cd /d "C:\Users\DELL\Downloads\Resume-Parser-OpenAI-main\Resume-Parser-OpenAI-main"
call venv\Scripts\activate
flask --app app.py run
pause