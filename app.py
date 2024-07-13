from flask import Flask
from tasks import send_email_task
from datetime import datetime
from flask import jsonify, request

app = Flask(__name__)

def logging(msg):
    with open("/var/log/messaging_system.log", "a") as log_file:
        log_file.write(f"{datetime.now()}: {msg}\n")

@app.route('/')
def index():
    if 'sendmail' in request.args:
        email = request.args.get('sendmail')
        try:
            logging(f"Sending mail to {email} ...")
            result = send_email_task.delay(email)
            logging(f"{result.get()}")
            return f"Email queued to be sent to {email} \n"
        except Exception as e:
            logging(f"Failed to send mail {e}")
            logging(f"{result.get()}")
    elif 'talktome' in request.args:
        logging("Request to talktome: Logged current time")
        return "Current time logged.\n"
    return "Welcome to @mustafaKane's messaging app\n"

@app.route('/logs')
def get_log():
    with open("/var/log/messaging_system.log", "r") as log_file:
        logs = log_file.read()
        return jsonify(logs)

if __name__ == '__main__':
    app.run(debug=True)
