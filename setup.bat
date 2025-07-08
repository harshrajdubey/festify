@echo off
echo 🎉 Welcome to Festify Setup!
echo ================================

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed. Please install Python 3.8+ first.
    pause
    exit /b 1
)

REM Check if pip is installed
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ pip is not installed. Please install pip first.
    pause
    exit /b 1
)

echo ✅ Prerequisites check passed!
echo.

REM Create virtual environment
echo 📦 Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo 🔄 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo 📥 Installing dependencies...
pip install -r requirements.txt

REM Create .env file if it doesn't exist
if not exist .env (
    echo 🔧 Creating .env file...
    copy .env.example .env
    echo ✅ .env file created! Please edit it with your database credentials.
    echo    File location: %cd%\.env
) else (
    echo ✅ .env file already exists.
)

echo.
echo 🚀 Setup complete!
echo.
echo Next steps:
echo 1. Edit the .env file with your database credentials
echo 2. Make sure PostgreSQL is running
echo 3. Create the database in PostgreSQL
echo 4. Run migrations: python manage.py migrate
echo 5. Start the server: python manage.py runserver
echo.
echo Happy coding! 🎨
pause
