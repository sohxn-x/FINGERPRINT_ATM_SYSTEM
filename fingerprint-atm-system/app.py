import os
import hashlib
from datetime import datetime
from flask import Flask, render_template, request, jsonify
from PIL import Image
import numpy as np

# Simulated Fingerprint Database
class FingerprintDatabase:
    def __init__(self):
        # Simulated users with fingerprints (fingerprint paths, PIN, and balance)
        self.users = {
            '1002': {
                'name': 'Mithun ',
                'fingerprint_path': 'fingerprints/1002.BMP',
                'account_balance': 5000.00,
                'pin': self.hash_pin('1234')
            },
            '1003': {
                'name': 'Kushal',
                'fingerprint_path': 'fingerprints/1003.BMP',
                'account_balance': 5500.00,
                'pin': self.hash_pin('5678')
            },
            '1004': {
                'name': 'Pruthviraj',
                'fingerprint_path': 'fingerprints/1004.BMP',
                'account_balance': 7000.00,
                'pin': self.hash_pin('1010')
            },
            '1005': {
                'name': 'Pruthvi K M',
                'fingerprint_path': 'fingerprints/1005.BMP',
                'account_balance': 2000.00,
                'pin': self.hash_pin('1111')
            },
            '1001': {
                'name': 'Manjunath',
                'fingerprint_path': 'fingerprints/1001.BMP',
                'account_balance': 7500.50,
                'pin': self.hash_pin('1100')
            }

        }

    def hash_pin(self, pin):
        # Hash the PIN using SHA256
        return hashlib.sha256(pin.encode()).hexdigest()

    def verify_fingerprint(self, user_id, fingerprint_image_path):
        # Compare the provided fingerprint image with the one stored for the user
        stored_fingerprint_path = self.users[user_id]['fingerprint_path']
        return self.compare_fingerprints(stored_fingerprint_path, fingerprint_image_path)

    def verify_pin(self, user_id, pin):
        # Verify the PIN by checking the stored hashed PIN
        return self.users[user_id]['pin'] == self.hash_pin(pin)

    def compare_fingerprints(self, stored_image_path, input_image_path):
        # Simulate comparing two fingerprint images
        try:
            stored_image = Image.open(stored_image_path)
            input_image = Image.open(input_image_path)
            return np.array_equal(np.array(stored_image), np.array(input_image))
        except Exception as e:
            print(f"Error comparing fingerprints: {e}")
            return False

# Transaction Logger
class TransactionLogger:
    def __init__(self, log_file='transactions.log'):
        self.log_file = log_file

    def log_transaction(self, user_id, transaction_type, amount):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"{timestamp} | User {user_id} | {transaction_type} | Rs {amount:.2f}\n"

        with open(self.log_file, 'a') as f:
            f.write(log_entry)

# ATM System Implementation
class ATMSystem:
    def __init__(self):
        self.db = FingerprintDatabase()
        self.logger = TransactionLogger()

    def authenticate(self, user_id, fingerprint_image_path, pin):
        # Perform two-factor authentication (fingerprint + PIN)
        fingerprint_match = self.db.verify_fingerprint(user_id, fingerprint_image_path)
        pin_match = self.db.verify_pin(user_id, pin)

        return fingerprint_match and pin_match

    def check_balance(self, user_id):
        # Return the user's account balance
        return self.db.users[user_id]['account_balance']

    def withdraw(self, user_id, amount):
        # Process withdrawal, check for sufficient funds
        user = self.db.users[user_id]
        if amount > user['account_balance']:
            return False, "Insufficient funds"

        user['account_balance'] -= amount
        self.logger.log_transaction(user_id, 'WITHDRAWAL', amount)

        return True, f"Withdrawn Rs {amount:.2f}"

    def deposit(self, user_id, amount):
        # Process deposit
        user = self.db.users[user_id]
        user['account_balance'] += amount
        self.logger.log_transaction(user_id, 'DEPOSIT', amount)

        return True, f"Deposited Rs {amount:.2f}"

# Flask Application
app = Flask(__name__)
atm = ATMSystem()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/authenticate', methods=['POST'])
def authenticate():
    user_id = request.form['userId']
    pin = request.form['pin']
    
    # Save uploaded fingerprint temporarily
    if 'fingerprint' not in request.files:
        return jsonify({'success': False, 'message': 'No fingerprint uploaded'})
    
    fingerprint = request.files['fingerprint']
    fingerprint_path = os.path.join('fingerprints', f'temp_{user_id}.bmp')
    fingerprint.save(fingerprint_path)

    # Authenticate
    if atm.authenticate(user_id, fingerprint_path, pin):
        # Remove temporary file
        os.remove(fingerprint_path)
        return jsonify({
            'success': True, 
            'message': 'Authentication Successful',
            'name': atm.db.users[user_id]['name'],
            'balance': atm.db.users[user_id]['account_balance']
        })
    
    # Remove temporary file
    os.remove(fingerprint_path)
    return jsonify({'success': False, 'message': 'Authentication Failed'})

@app.route('/withdraw', methods=['POST'])
def withdraw():
    user_id = request.form['userId']
    amount = float(request.form['amount'])
    
    success, message = atm.withdraw(user_id, amount)
    return jsonify({
        'success': success, 
        'message': message,
        'balance': atm.check_balance(user_id)
    })

@app.route('/deposit', methods=['POST'])
def deposit():
    user_id = request.form['userId']
    amount = float(request.form['amount'])
    
    success, message = atm.deposit(user_id, amount)
    return jsonify({
        'success': success, 
        'message': message,
        'balance': atm.check_balance(user_id)
    })

@app.route('/check_balance', methods=['POST'])
def check_balance():
    user_id = request.form['userId']
    
    # Check if the user exists
    if user_id not in atm.db.users:
        return jsonify({'success': False, 'message': 'User not found'})

    # Get the current balance
    balance = atm.check_balance(user_id)
    
    return jsonify({
        'success': True,
        'message': 'Balance fetched successfully',
        'balance': balance
    })

if __name__ == '__main__':
    # Ensure fingerprints directory exists
    os.makedirs('fingerprints', exist_ok=True)
    app.run(debug=True)

