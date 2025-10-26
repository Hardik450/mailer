
***

# Django REST Email Sender API

A simple, scalable Django REST API to send emails asynchronously. Features instant API response (non-blocking) using Python threading, and is suitable for free deployment and moderate loads. Easily integrable with any frontend (React, HTML/JS, etc).

***

## Features

- **POST /mailer/send-email/**  
  Send an email using subject, message, and recipient in the JSON body.
- **Asynchronous Email Sending**  
  Uses `threading.Thread` so requests return instantly—even during slow SMTP operations.
- **Input Validation & Error Handling**  
  Returns informative error messages and appropriate HTTP response codes.

***

## Quickstart

### 1. Clone & Install

```bash
git clone https://github.com/Hardik450/mailer.git
cd email_service
python -m venv venv
source venv/bin/activate  # on Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Settings

In `email_service/settings.py`, set your SMTP credentials. For Gmail:

```python
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "<your_gmail>@gmail.com"
EMAIL_HOST_PASSWORD = "<your_app_password>"
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
```

> **Tip:** For production/testing, consider free transactional providers (e.g. Mailtrap, SendGrid).

### 3. Migrate & Run

```bash
python manage.py migrate
python manage.py runserver
```

***

## API Usage

### POST /mailer/send-email/

Send JSON data:
```json
{
  "subject": "Sample Subject",
  "message": "Hello from the Django REST email API.",
  "recipient_list": "someone@example.com"
}
```

**Sample Request (cURL):**
```bash
curl -X POST http://127.0.0.1:8000/mailer/send-email/ \
  -H "Content-Type: application/json" \
  -d '{"subject": "Hi", "message": "This is a test", "recipient_list": "user@gmail.com"}'
```

**Response:**
- `200 OK`  
  ```json
  {"success": "Email is being sent in the background."}
  ```
- `400 Bad Request` if fields are missing
- `500 Internal Server Error` on unexpected errors

***

## How It Works

- Incoming POST requests are validated.
- The API instantly starts a **background thread** to send the email with Django’s `send_mail`.
- The user receives “email is being sent” message without waiting for SMTP completion.
- SMTP exceptions are logged; API remains responsive.

***




**Troubleshooting**

- If you receive emails in Spam/Promotions: adjust SMTP credentials, use a verified sender, or try transactional mail APIs.
- Error 400? Ensure JSON keys and values are correctly named and sent.
- For local-only development, use Django’s console backend for debugging.

***

