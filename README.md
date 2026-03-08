# Secure Notes App

A secure web application for storing personal notes, built with Flask. Created as part of the *Data Protection* course at Warsaw University of Technology.

## Features

- **User authentication** — email + password login with Argon2id hashing
- **Two-factor authentication (2FA)** — TOTP via Google Authenticator (QR code setup)
- **Encrypted secrets** — TOTP secrets stored encrypted with AES-CFB + PBKDF2 key derivation
- **XSS protection** — notes support Markdown rendering, sanitized with `bleach` before display
- **Brute-force protection** — exponential delay + account lockout after 5 failed attempts
- **HTTPS** — served via Nginx reverse proxy with SSL/TLS

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Flask (Python) |
| Password hashing | Argon2id (`argon2-cffi`) |
| 2FA | TOTP (`pyotp`) |
| Encryption | AES-CFB (`pycryptodome`) |
| Sanitization | `bleach` + `markdown` |
| Deployment | Docker + Nginx |

## Project Structure

```
Project2/
├── app/
│   ├── hello.py          # Routes: home, notes (add/view/delete)
│   ├── login.py          # Login flow: password + TOTP, brute-force protection
│   ├── regestration.py   # Registration + TOTP setup
│   ├── aes.py            # AES-CFB encrypt/decrypt helpers
│   ├── database.py       # SQLite database operations
│   ├── templates/        # Jinja2 HTML templates
│   └── .env              # Secret keys (not committed)
├── nginx/
│   ├── nginx.conf        # Reverse proxy + SSL config
│   └── certs/            # SSL certificate & key
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

## Running the App

```bash
docker-compose up --build
```

Then open `https://localhost` in your browser.

> **Note:** The app uses a self-signed certificate by default. Accept the browser warning or replace `nginx/certs/` with your own certificate.

## Security Overview

- Passwords hashed with **Argon2id** (resistant to GPU/side-channel attacks)
- TOTP secrets encrypted with **AES-CFB** using a PBKDF2-derived key and random IV/salt per user
- Login is blocked for **5 minutes** after 5 failed attempts, with **exponential delay** between tries
- Markdown notes are rendered then stripped of dangerous HTML tags via **bleach whitelist**
- All traffic forced through **HTTPS** via Nginx

