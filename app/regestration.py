from flask import Flask, render_template, request, session, redirect, url_for
from argon2 import PasswordHasher
import database
import pyotp
import qrcode
import os
from aes import encrypt_aes

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET', 'Xasfg3hgjyewktwtn')
ph = PasswordHasher()



@app.route("/register", methods=['GET', 'POST'])
def register():

    if request.method == "GET":
        return render_template("register.html")

    email = request.form.get("email")
    password = request.form.get("password")
    password2 = request.form.get("password2")
    #Walidacja Emaila
    if not email or not password or not password2:
        return render_template("register.html", error="Brak danych: email lub password")
    if not valid_email(email):
        return render_template("register.html", error="Niepoprawny email")


    #Walidacja password

    if password != password2:
        return render_template("register.html", error="Hasła różnią się")
    if len(password) < 8:
        return render_template("register.html", error="Hasła za krótkie")

    #Istnienie Usera

    existing_user = database.get_user_by_username(email)
    if existing_user:
        return render_template("register.html", error="Ten user już istnieje")

    password_hash = ph.hash(password)

    session['email'] = email
    session['password_hash'] = password_hash

    return redirect(url_for('setup_totp'))


@app.route("/setup-totp", methods=['GET', 'POST'])
def setup_totp():

    if 'email' not in session:
        return redirect(url_for('register'))

    email = session['email']

    if request.method == "GET":
        totp_secret = pyotp.random_base32()
        session['totp_secret'] = totp_secret
        qr_path = create_qr(email, totp_secret)
        session['qr_path'] = qr_path
        return render_template("setup_totp.html", qr_path=qr_path)

    totp_secret = session['totp_secret']

    code = request.form.get("code")
    qr_path=session.get('qr_path')
    if not code:
        
        return render_template("setup_totp.html", qr_path=qr_path, error="Wpisz kod")

    totp = pyotp.TOTP(totp_secret)
    kod_ok = totp.verify(code)

    if not kod_ok:
        qr_path = create_qr(email, totp_secret)
        return render_template("setup_totp.html", qr_path=qr_path,  error="Zly kod")

    password_hash = session['password_hash']

    aes_secret, iv, salt = encrypt_aes(totp_secret)
    user_id = database.create_user(email, password_hash, aes_secret, iv, salt)

    session.pop("qr_path", None)
    delete_qr(email)

    session.pop('email', None)
    session.pop('password_hash', None)
    session.pop('totp_secret', None)

    if user_id:
        return redirect(url_for("login_password"))
    else:
        return render_template("setup_totp.html", error="Cos poszlo zle")


def create_qr(email, totp_secret):
    base_dir = os.path.dirname(os.path.abspath(__file__)) #Korzeń
    static_dir = os.path.join(base_dir, "static", "qr_codes")

    os.makedirs(static_dir, exist_ok=True)

    totp = pyotp.TOTP(totp_secret)
    uri = totp.provisioning_uri(name=email, issuer_name="project2")
    img = qrcode.make(uri)

    safe_email = email.replace("@", "_").replace(".", "_")
    filename = f"user_{safe_email}.png"

    full_path = os.path.join(static_dir, filename)
    img.save(full_path)

    return f"static/qr_codes/{filename}"


def delete_qr(email):
    base_dir = os.path.dirname(os.path.abspath(__file__))

    safe_email = email.replace("@", "_").replace(".", "_")
    filename = f"user_{safe_email}.png"

    qr_path = os.path.join(base_dir, "static", "qr_codes", filename)

    if os.path.exists(qr_path):
        os.remove(qr_path)


def valid_email(email):
    return '@' in email and '.' in email


import login
import hello

database.init_database()

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
