# Email Configuration Guide

## Current Setup (Development)
The project is currently configured to use Django's **Console Email Backend**, which prints emails to the console instead of actually sending them. This is perfect for development and testing.

When a student registers, you'll see the email output in your Django development server console.

## How to Test Email During Development

1. Start the Django development server:
```cmd
python manage.py runserver
```

2. Go to the registration page: http://127.0.0.1:8000/register/

3. Fill out the form and submit

4. Check the Django console - you'll see the email content printed there:
```
Content-Type: text/plain; charset="utf-8"
MIME-Version: 1.0
Content-Transfer-Encoding: 7bit
Subject: Welcome to Our School
From: webmaster@localhost
To: student@example.com
Date: ...

Thank you for choosing our school
```

## Setup for Production (Send Real Emails)

To send real emails via Gmail or another SMTP server, edit `settings.py` and uncomment the production email configuration:

### For Gmail:
1. Go to Google Account Security settings
2. Enable "App passwords" and generate one
3. Update `settings.py`:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-16-char-app-password'
DEFAULT_FROM_EMAIL = 'your-email@gmail.com'
```

### For Other SMTP Providers:
Update the EMAIL_HOST and EMAIL_PORT accordingly (e.g., Office 365, SendGrid, etc.)

## Current Email Features
✅ Welcome email sent automatically on student registration
✅ Email contains: "Thank you for choosing our school"
✅ Error handling: If email fails, the registration still completes successfully

## Testing with Real SMTP
For testing with a real SMTP account without using your actual email, consider:
- **Mailtrap.io** - Free email testing service
- **SendGrid** - Free tier available
- **Mailgun** - Free tier available

These services provide SMTP credentials that you can use for testing production email setup.
