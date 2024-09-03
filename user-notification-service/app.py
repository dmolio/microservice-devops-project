from flask import Flask, request, jsonify
from flask_mail import Mail, Message
from celery import Celery
import os

app = Flask(__name__)

# Configuring Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.example.com'  # Replace with your SMTP server
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')

mail = Mail(app)

# Configure Celery
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

@celery.task
def send_async_email(msg_data):
    with app.app_context():
        msg = Message(**msg_data)
        mail.send(msg)

@app.route('/notify', methods=['POST'])
def notify_user():
    data = request.json
    msg_data = {
        'subject': data['subject'],
        'sender': app.config['MAIL_USERNAME'],
        'recipients': [data['email']],
        'body': data['message']
    }
    send_async_email.delay(msg_data)
    return jsonify({"status": "Notification is being sent"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
