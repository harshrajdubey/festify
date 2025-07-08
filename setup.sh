#!/bin/bash

# Festify Quick Setup Script
# This script helps you set up the Festify project quickly

echo "🎉 Welcome to Festify Setup!"
echo "================================"

# Check if Python is installed
if ! command -v python &> /dev/null; then
    echo "❌ Python is not installed. Please install Python 3.8+ first."
    exit 1
fi

# Check if pip is installed
if ! command -v pip &> /dev/null; then
    echo "❌ pip is not installed. Please install pip first."
    exit 1
fi

# Check if PostgreSQL is installed
if ! command -v psql &> /dev/null; then
    echo "⚠️  PostgreSQL is not installed. Please install PostgreSQL first."
    echo "   You can download it from: https://www.postgresql.org/download/"
    exit 1
fi

echo "✅ Prerequisites check passed!"
echo ""

# Create virtual environment
echo "📦 Creating virtual environment..."
python -m venv venv

# Activate virtual environment
echo "🔄 Activating virtual environment..."
if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "🔧 Creating .env file..."
    cp .env.example .env
    echo "✅ .env file created! Please edit it with your database credentials."
    echo "   File location: $(pwd)/.env"
else
    echo "✅ .env file already exists."
fi

echo ""
echo "🚀 Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit the .env file with your database credentials"
echo "2. Make sure PostgreSQL is running"
echo "3. Create the database: createdb festify"
echo "4. Run migrations: python manage.py migrate"
echo "5. Start the server: python manage.py runserver"
echo ""
echo "Happy coding! 🎨"
