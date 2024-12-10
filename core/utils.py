import threading
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
import random
import string

def generate_password(length=8):
    characters = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(random.choice(characters) for _ in range(length))

def send_user_credentials(request, user, first_name, last_name):
    # Generate a random password
    password = generate_password()
    user.set_password(password)
    user.save()
    
    # Prepare email data
    subject = "Welcome to Our Company"
    context = {
        'company_name': user.company.name,
        'employee_name': first_name + ' ' + last_name,
        'username': user.username,
        'password': password,
        'login_url': request.build_absolute_uri(f'/login/'),
        'year': 2024,
    }
    message = render_to_string('email/employee_welcome_email.html', context)
    
    # Send the email asynchronously using a separate thread
    def send_email():
        email = EmailMessage(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
        email.content_subtype = 'html'  # Send as HTML email
        email.send()

    # Start the email-sending process in a new thread
    email_thread = threading.Thread(target=send_email)
    email_thread.start()
