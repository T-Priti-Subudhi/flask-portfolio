from flask import Flask, render_template, request, redirect, url_for,flash, get_flashed_messages
from flask_mail import Mail, Message
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')  # Secure way
# ---- Mail Config ----
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")
app.config['MAIL_DEFAULT_SENDER'] = os.getenv("MAIL_USERNAME") # ✅ Required to fix your error


mail = Mail(app)

@app.route('/')
def home():
    return render_template("index.html")

from flask import flash, get_flashed_messages

@app.route('/thankyou', methods=['GET', 'POST'])
def thank_you():
    if request.method == 'POST':
        name = request.form.get('fullname', '')
        email = request.form.get('email', '')
        mobile = request.form.get('mobile', '')
        message = request.form.get('message', '')

        # Check if required fields are filled
        if not name or not email or not message:
            flash("Please fill all required fields.", "error")
            return redirect(url_for('home'))

        msg = Message(
            subject="New Contact from Portfolio",
            recipients=['your_email@gmail.com'],
            body=f"Name: {name}\nEmail: {email}\nMobile: {mobile}\nMessage: {message}"
        )

        mail.send(msg)
        flash("Your message has been sent successfully!", "success")
        return render_template("thankyou.html", name=name)

    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
