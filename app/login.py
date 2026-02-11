from flask import render_template, request, session, redirect, url_for
from argon2 import PasswordHasher, exceptions
from database import get_user_by_username, update_failed_attempts, reset_failed_attempts
from aes import decrypt_aes
import pyotp
import time

from regestration import app

ph = PasswordHasher()
max_attempts = 5
block = 300 
max_delay=8


@app.route("/login_password", methods=['GET', 'POST'])
def login_password():
    if request.method == "GET":
        return render_template("login_password.html")

    email = request.form.get("email")
    password = request.form.get("password")

    if not email or not password:
        return render_template("login_password.html", error="Wpisz email i haslo")
    if not valid_email(email):
        return render_template("login_password.html", error="Niepoprawny email")

    user = get_user_by_username(email)
    if not user:
        return render_template("login_password.html", error="Zly email lub haslo")

    
    if user['locked_until'] > time.time():
        pozostalo = int(user['locked_until'] - time.time())
        return render_template("login_password.html", error=f"Konto zablokowane na {pozostalo} sekund")

 
    try:
        ph.verify(user['password_hash'], password)
    except Exception:
        new_attempts = user['failed_attempts'] + 1
        #return render_template("login_password.html", error="Zly email lub haslo")
        time.sleep(delay(new_attempts))
        if new_attempts >= max_attempts:
            locked_until = time.time() + block
            update_failed_attempts(email, new_attempts, locked_until)
            return render_template("login_password.html", error=f" {block} zablokowany")

        update_failed_attempts(email, new_attempts)
        return render_template("login_password.html", error="Zly email lub haslo")

    session['email']=email

    return render_template("login_totp.html", email=email)


@app.route("/login_totp", methods=['POST'])
def login_totp():
    
    
    if 'email' not in session:
            return redirect(url_for('register'))
    email=session['email']
    
    code = request.form.get("code")

    if not email:
        return redirect(url_for('login_password'))

    user = get_user_by_username(email)
    if not user:
        return redirect(url_for('login_password'))

    
    if user['locked_until'] > time.time():
        return redirect(url_for('login_password'))

    if not code:
        new_attempts = user['failed_attempts'] + 1
        time.sleep(delay(new_attempts))
        update_failed_attempts(email, new_attempts)
        return render_template("login_totp.html", email=email, error="Wpisz kod")

    totp_secret = decrypt_aes(user['totp_secret'], user['totp_iv'], user['totp_salt'])
    totp = pyotp.TOTP(totp_secret)

    if not totp.verify(code):
        new_attempts = user['failed_attempts'] + 1
        time.sleep(delay(new_attempts))
        
        if new_attempts >= max_attempts:
            locked_until = time.time() + block
            update_failed_attempts(email, new_attempts, locked_until)
            return redirect(url_for('login_password'))

        update_failed_attempts(email, new_attempts)
        return render_template("login_totp.html", email=email, error="Zly kod")

   
    reset_failed_attempts(email)

    session['user_id'] = user['id']

    return redirect(url_for('home'))


def delay(failed_attempts):
    return min(2**failed_attempts, max_delay)


def valid_email(email):
    return '@' in email and '.' in email




@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('login_password'))


