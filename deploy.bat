@echo off
setlocal enabledelayedexpansion
:: BatchGotAdmin
:-------------------------------------
REM  --> Check for permissions
IF "%PROCESSOR_ARCHITECTURE%" EQU "amd64" (
    >nul 2>&1 "%SYSTEMROOT%\SysWOW64\cacls.exe" "%SYSTEMROOT%\SysWOW64\config\system"
) ELSE (
    >nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system"
)

REM --> If error flag set, we do not have admin.
if '%errorlevel%' NEQ '0' (
    echo Requesting administrative privileges...
    goto UACPrompt
) else (
    goto gotAdmin
)

:UACPrompt
    REM Create a VBScript to request administrative privileges
    echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"
    set params= %*
    echo UAC.ShellExecute "cmd.exe", "/c ""%~s0"" %params:"=""%", "", "runas", 1 >> "%temp%\getadmin.vbs"

    REM Execute the VBScript
    "%temp%\getadmin.vbs"
    del "%temp%\getadmin.vbs"
    exit /B

:gotAdmin
    pushd "%CD%"
    CD /D "%~dp0"
:--------------------------------------
echo This Script is for auto deploy IoTAppBackend Project

REM 檢查是否安裝了 Python 3.10.0
where python >nul 2>nul
if %errorlevel% equ 0 (
    for /f "tokens=2" %%i in ('python --version 2^>^&1') do set pyversion=%%i
	if "!pyversion!" neq "3.10.0" (
		echo Python version is !pyversion!, not 3.10.0
		goto InstallPython
	) else (
		echo Python 3.10.0 is already installed
		goto installGit
	)
) else (
    goto InstallPython
)

:InstallPython
echo Downloading and installing Python 3.10.0...
if not exist "python-3.10.0-amd64.exe" (
	powershell -Command "wget https://www.python.org/ftp/python/3.10.0/python-3.10.0-amd64.exe -OutFile python-3.10.0-amd64.exe"
)
echo Installing Python 3.10.0...
start /wait python-3.10.0-amd64.exe /quiet InstallAllUsers=1 PrependPath=1
echo Python 3.10.0 installed.

:installGit
REM 檢查是否安裝了 Git
where git >nul 2>nul

REM 如果沒有安裝 Git，則下載並安裝
if %errorlevel% neq 0 (
    echo Git not found. Downloading and installing...
	if not exist "Git-2.45.2-64-bit.exe" (
		powershell -Command "wget https://github.com/git-for-windows/git/releases/download/v2.45.2.windows.1/Git-2.45.2-64-bit.exe -OutFile Git-2.45.2-64-bit.exe"
	)
    echo Installing Git...
    start /wait Git-2.45.2-64-bit.exe /VERYSILENT /NORESTART
    echo Git installed.
) else (
    echo Git is already installed.
)

REM 克隆專案
set "PATH=%PATH%;C:\Program Files\Git\cmd;C:\Program Files\Python310\;C:\Program Files\Python310\Scripts\"
echo Cloning the project repository...
if not exist "IoTAppBackEnd" (
    git clone https://github.com/silver0416/IoTAppBackEnd.git
) else (
    echo Repository already exists. Skipping clone.
)

REM 更新 pip 並安裝 virtualenv
echo Installing and setting up virtual environment...
python -m pip install -U pip
pip install virtualenv

REM 建立虛擬環境並激活
if not exist "myenv310" (
    virtualenv -p python3.10 myenv310
)
call myenv310\Scripts\activate.bat

REM 確認虛擬環境已激活
if "%VIRTUAL_ENV%" == "" (
    echo Failed to activate virtual environment.
    exit /b 1
) else (
    echo Virtual environment activated.
)

REM 虛擬環境部署相關依賴包
cd IoTAppBackEnd
python.exe -m pip install --upgrade pip
pip install -r requirements.txt

REM 從上兩級目錄複製 secret.yml 文件到當前目錄
cd app
if exist "..\..\secret.yml" (
    xcopy ..\..\secret.yml .\ /Y
) else (
    echo Warning: secret.yml not found in the parent directory.
)

REM 啟動 Django 伺服器
set DATABASE_NAME=databasename
set DATABASE_USER=databaseuser
set DATABASE_PASSWORD=databasepassword
set DATABASE_HOST=databaseip
set DATABASE_PORT=3306
python manage.py makemigrations
python manage.py migrate
echo Starting Django server...
python manage.py runserver 0.0.0.0:8701

REM 暫停以查看輸出
pause
exit /b 0
