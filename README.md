# Festify 🎉

A Django-based web application for creating beautiful templates for birthdays, weddings, portfolios, and more. Customize them easily and share with the world.

## Features

- **User Authentication**: Registration, login, and phone number verification via OTP
- **Template Creation**: Create stunning templates for various occasions
- **Visual Editor**: Customize templates with an intuitive interface
- **Easy Sharing**: Share your creations with unique URLs
- **Phone Verification**: Secure OTP-based phone number verification
- **Responsive Design**: Modern UI built with Tailwind CSS

## Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.8 or higher
- PostgreSQL database
- Git

## Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/shashiX07/festify.git
cd festify
```

### 2. Create a Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
# Install production dependencies
pip install -r requirements.txt

# For development (optional)
pip install -r requirements-dev.txt
```

### 4. Environment Configuration

Create a `.env` file in the project root directory by copying from the example:

```bash
# Copy the example environment file
cp .env.example .env
```

Edit the `.env` file with your database credentials:

```env
DB_NAME="festify"
DB_USER="your_postgres_username"
DB_PASSWORD="your_postgres_password"
DB_HOST="localhost"
DB_PORT="5432"
```

**Important**: Replace the values with your actual PostgreSQL credentials.

### 5. Database Setup

Make sure PostgreSQL is running and create the database:

```sql
-- Connect to PostgreSQL as superuser
psql -U postgres

-- Create database
CREATE DATABASE festify;

-- Create user (optional, if you want a specific user)
CREATE USER your_username WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE festify TO your_username;
```

### 6. Run Migrations

```bash
# Make migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate
```

### 7. Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

### 8. Run the Development Server

```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`

## Project Structure

```
festify/
├── manage.py
├── requirements.txt
├── requirements-dev.txt
├── .env.example
├── .env                    # Create this file
├── .gitignore
├── README.md
├── festify/                # Main project directory
│   ├── __init__.py
│   ├── settings.py         # Project settings
│   ├── urls.py            # URL configuration
│   ├── views.py           # Main views
│   ├── wsgi.py
│   └── asgi.py
├── users/                  # User authentication app
│   ├── models.py          # User model with OTP verification
│   ├── views.py           # Authentication views
│   ├── forms.py           # User forms
│   ├── urls.py            # User URLs
│   ├── admin.py
│   ├── apps.py
│   ├── tests.py
│   ├── migrations/
│   └── templates/
│       └── users/
│           ├── base.html
│           ├── login.html
│           ├── register.html
│           ├── profile.html
│           └── verify_otp.html
└── templates/
    └── festify/
        └── home.html
```

## Usage

### 1. Home Page

Visit `http://127.0.0.1:8000/` to see the landing page.

### 2. User Registration

- Go to `/register/` to create a new account
- Fill in username, email, phone number, and password
- Verify your phone number with the OTP sent

### 3. User Login

- Go to `/login/` to log into your account
- If your phone number isn't verified, you'll be redirected to OTP verification

### 4. Profile

- After logging in, access your profile at `/{username}/`
- View your account information and verification status

## API Endpoints

- `/` - Home page
- `/register/` - User registration
- `/login/` - User login
- `/logout/` - User logout
- `/verify-otp/` - OTP verification
- `/resend-otp/` - Resend OTP (AJAX endpoint)
- `/{username}/` - User profile page
- `/admin/` - Django admin interface

## Environment Variables

Create a `.env` file with the following variables:

```env
# Database Configuration
DB_NAME="festify"
DB_USER="your_postgres_username"
DB_PASSWORD="your_postgres_password"
DB_HOST="localhost"
DB_PORT="5432"

# Add these for production (optional)
# SECRET_KEY="your-secret-key"
# DEBUG=False
# ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

## Development

### Running Tests

```bash
# Run all tests
python manage.py test

# Run tests with coverage (if you installed dev requirements)
pytest --cov=.
```

### Code Formatting

```bash
# Format code with black
black .

# Sort imports
isort .

# Lint code
flake8 .
```

### Django Commands

```bash
# Create new migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files (for production)
python manage.py collectstatic

# Run development server
python manage.py runserver
```

## Production Deployment

### 1. Environment Setup

- Set `DEBUG=False` in `.env`
- Configure `ALLOWED_HOSTS` in `.env`
- Set up a production-grade database
- Configure static file serving

### 2. Security

- Generate a secure `SECRET_KEY`
- Use HTTPS in production
- Configure proper CORS settings
- Set up environment-specific settings

### 3. Database

- Use PostgreSQL in production
- Run migrations on production database
- Set up database backups

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Troubleshooting

### Common Issues

**Database Connection Error:**

- Ensure PostgreSQL is running
- Check database credentials in `.env`
- Verify database exists

**OTP Not Working:**

- Check if phone number format is correct
- Verify OTP expiration time (5 minutes)
- Check rate limiting (max 5 OTPs per day)

**Static Files Not Loading:**

- Run `python manage.py collectstatic`
- Check `STATIC_URL` and `STATIC_ROOT` settings

**Migration Errors:**

- Delete migration files and run `makemigrations` again
- Check for model conflicts
- Ensure database is accessible

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please open an issue on the [GitHub repository](https://github.com/shashiX07/festify/issues).

## Acknowledgments

- Built with Django and Tailwind CSS
- Icons from various sources
- Inspiration from modern template builders

---

**Happy Templating with Festify! 🎨✨**
