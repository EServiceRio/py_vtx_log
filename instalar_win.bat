@ECHO OFF

call:cor f1 "instalado componentes"

timeout /t 10

pip install django django-cors-headers pymodbus==2.5.2

call:cor f1 "verifique se nao ocorreu erros"

timeout /t 60

call:cor f1 "criando os arquivos de inicialização na area de trabalho e de inicializaçao do SO"

type NUL > VT.bat
chcp 65001 > nul
echo start chrome --kiosk --fullscreen http://localhost:8000 > VT.bat
echo cd /d %cd%\backend >> VT.bat
echo python manage.py runserver 0.0.0.0:8000 >> VT.bat

set /p desk="Gostaria de criar atalho na area de trabalho (s)/(n)"

if %desk% equ s (copy "VT.bat" "c:\%HOMEPATH%\Desktop")

set /p startup="Gostaria de iniciar junto do windowns (s)/(n)"

if %startup% equ s (copy "c:\%HOMEPATH%\Desktop\VT.bat" "%appdata%\Microsoft\windows\start menu\programs\startup")

set /p valor="deseja iniciar o supervisorio (s)/(n)"

if %valor% equ n (GOTO :fim)

if %valor% equ N (GOTO :fim)

call:cor f1 "inicinado o supervisorio aguarade..."

start chrome --kiosk --fullscreen http://localhost:8000

cd backend

python manage.py runserver 0.0.0.0:8000

exit
:cor
>%2 (set/p=.) <&1
findstr /a:%1 . %2 con &erase %2
for /f "delims=" %%a in ('cmd /k prompt $h$h ^<^&1') do echo %%a
goto:eof

:fim