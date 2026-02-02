# 🏦 Fingerprint ATM System (Flask-Based)

A **Flask web application** that simulates an ATM system secured using **two-factor authentication**:  
**Fingerprint image verification + PIN authentication**.  
The system allows authenticated users to perform basic banking operations such as **balance inquiry, cash withdrawal, and deposit**, with all transactions securely logged.

> ⚠️ This project is a **simulation for academic and demonstration purposes**. It does **not implement real biometric fingerprint matching**.

---

## 🚀 Features

- 🔐 **Two-Factor Authentication**
  - Fingerprint image matching (simulated)
  - Secure PIN verification using SHA-256 hashing

- 🏧 **ATM Operations**
  - Check account balance
  - Withdraw money (with insufficient balance checks)
  - Deposit money

- 🧾 **Transaction Logging**
  - All deposits and withdrawals are timestamped
  - Stored in a transaction log file for auditing

- 🌐 **Web-Based Interface**
  - Built using Flask, HTML templates, and REST-style endpoints

---

## 🧠 System Architecture

The project follows a **modular and layered design**:

Fingerprint_ATM_System/
│
├── app.py # Main Flask application
├── fingerprints/ # Stored fingerprint images (BMP format)
├── templates/
│ └── index.html # Frontend UI
├── static/
│ └── index.html # Static assets
├── transactions.log # Transaction history
└── README.md


---

## 🔑 Authentication Workflow

1. User enters:
   - User ID
   - PIN
   - Fingerprint image
2. Fingerprint is temporarily stored and compared with the registered fingerprint
3. PIN is hashed using **SHA-256** and verified
4. Access is granted only if **both fingerprint and PIN match**
5. Temporary fingerprint file is deleted after authentication

---

## 🧪 Fingerprint Matching (Simulation)

Fingerprint verification is simulated using **pixel-by-pixel comparison**:

```python
np.array_equal(stored_image, input_image)
