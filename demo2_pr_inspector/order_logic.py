import os
import subprocess
import pickle
import json
import sqlite3
from flask import request
import requests

# ========== CRITICAL SEVERITY ISSUES ==========

# 1. Command injection vulnerability (CRITICAL)
def execute_system_command(user_input):
    """Critical: Command injection vulnerability"""
    # NEVER DO THIS - user input directly in system command
    os.system(f"echo {user_input}")  # CRITICAL: Command injection
    
    # Also vulnerable
    subprocess.call(f"ls {user_input}", shell=True)  # CRITICAL: Shell injection

# 2. Insecure deserialization (CRITICAL)
def load_user_data(serialized_data):
    """Critical: Insecure deserialization"""
    # NEVER DO THIS - pickle can execute arbitrary code
    return pickle.loads(serialized_data)  # CRITICAL: Arbitrary code execution

# 3. Hardcoded secrets (CRITICAL)
AWS_ACCESS_KEY = "AKIAIOSFODNN7EXAMPLE"
AWS_SECRET_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
DATABASE_PASSWORD = "SuperSecret123!"

# ========== HIGH SEVERITY ISSUES ==========

# 4. SQL injection (HIGH)
def get_user_data(user_id):
    """High: SQL injection vulnerability"""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # NEVER DO THIS - SQL injection
    query = f"SELECT * FROM users WHERE id = {user_id}"  # HIGH: SQL injection
    cursor.execute(query)
    
    return cursor.fetchall()

# 5. Insecure direct object reference (HIGH)
def get_user_file(filename):
    """High: Path traversal vulnerability"""
    # NEVER DO THIS - Path traversal
    with open(f"/home/user/files/{filename}", "r") as f:  # HIGH: Path traversal
        return f.read()

# 6. XXE vulnerability (HIGH)  
def parse_xml(xml_data):
    """High: XXE vulnerability"""
    # In a real XML parser, this would be vulnerable to XXE
    # For demo purposes, we'll just show the pattern
    return f"Parsed XML: {xml_data}"

# ========== MEDIUM SEVERITY ISSUES ==========

# 7. Business logic flaw (MEDIUM)
def update_delivery_date(order_id, new_date):
    """Medium: Missing order status validation"""
    # Missing check if order is already shipped
    # This allows modifying delivery dates for shipped orders
    return {"status": "updated", "new_date": new_date}

# 8. Insecure randomness (MEDIUM)
def generate_session_token():
    """Medium: Weak random number generation"""
    import random
    return random.randint(1000, 9999)  # MEDIUM: Predictable random numbers

# 9. Missing input validation (MEDIUM)
def process_payment(amount, card_number):
    """Medium: Missing input validation"""
    # No validation of amount (could be negative)
    # No validation of card number format
    return f"Processed ${amount} from card {card_number}"

# ========== LOW SEVERITY ISSUES ==========

# 10. Information disclosure (LOW)
def debug_error(error_message):
    """Low: Information disclosure in error messages"""
    # Exposing internal details in error messages
    raise Exception(f"Database error: Connection failed to {DATABASE_PASSWORD}@{os.environ.get('DB_HOST', 'localhost')}")

# 11. Missing security headers (LOW)
def create_http_response(content):
    """Low: Missing security headers"""
    # In a real web app, missing security headers like:
    # - Content-Security-Policy
    # - X-Frame-Options
    # - X-Content-Type-Options
    return {"content": content}

# 12. Verbose error messages (LOW)
def divide_numbers(a, b):
    """Low: Verbose error messages"""
    try:
        return a / b
    except Exception as e:
        # Exposing too much information
        return f"Error in division: {type(e).__name__}: {str(e)}. Stack trace: {e.__traceback__}"

# ========== ADDITIONAL VULNERABILITIES FOR DEMO ==========

# 13. Use of deprecated/weak crypto (HIGH)
def encrypt_password(password):
    """High: Weak encryption (MD5)"""
    import hashlib
    return hashlib.md5(password.encode()).hexdigest()  # HIGH: Weak hash

# 14. Insecure cookie handling (MEDIUM)
def set_auth_cookie(user_id):
    """Medium: Insecure cookie flags"""
    # Missing HttpOnly, Secure, SameSite flags
    return f"auth_token={user_id}"

# 15. CORS misconfiguration (MEDIUM)
def handle_cors_request():
    """Medium: Overly permissive CORS"""
    # Allows any origin
    return {"Access-Control-Allow-Origin": "*"}

# Main function to demonstrate vulnerabilities
def main():
    print("Demo application with security vulnerabilities")
    
    # Demonstrate command injection
    user_input = input("Enter your name: ")
    execute_system_command(user_input)
    
    # Demonstrate business logic flaw
    order_result = update_delivery_date(123, "2024-12-31")
    print(f"Order update result: {order_result}")
    
    # Demonstrate SQL injection
    user_data = get_user_data("1 OR 1=1")
    print(f"User data: {user_data}")

if __name__ == "__main__":
    main()