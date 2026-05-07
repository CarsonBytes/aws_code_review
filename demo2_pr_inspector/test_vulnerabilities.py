#!/usr/bin/env python3
"""
Test script to demonstrate security vulnerabilities in demo2.
This script is intentionally vulnerable for Amazon Inspector testing.
"""

import os
import sys
import pickle

def test_command_injection():
    """Test command injection vulnerability"""
    print("Testing command injection...")
    user_input = "test; echo 'INJECTED'"
    os.system(f"echo {user_input}")
    return True

def test_sql_injection():
    """Test SQL injection pattern"""
    print("Testing SQL injection pattern...")
    user_id = "1 OR 1=1"
    query = f"SELECT * FROM users WHERE id = {user_id}"
    print(f"Vulnerable query: {query}")
    return True

def test_insecure_deserialization():
    """Test insecure deserialization"""
    print("Testing insecure deserialization...")
    # Create a malicious pickle object
    class Malicious:
        def __reduce__(self):
            return (os.system, ('echo "PICKLE EXPLOIT"',))
    
    malicious_pickle = pickle.dumps(Malicious())
    print(f"Created malicious pickle object: {len(malicious_pickle)} bytes")
    return True

def test_hardcoded_secrets():
    """Test hardcoded secrets detection"""
    print("Testing hardcoded secrets...")
    aws_key = "AKIAIOSFODNN7EXAMPLE"
    aws_secret = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
    db_password = "SuperSecret123!"
    
    print(f"AWS Key: {aws_key[:10]}...")
    print(f"AWS Secret: {aws_secret[:10]}...")
    print(f"DB Password: {db_password[:10]}...")
    return True

def test_business_logic_flaw():
    """Test business logic vulnerability"""
    print("Testing business logic flaw...")
    
    def update_delivery_date(order_id, new_date):
        # Missing order status check
        return {"status": "updated", "new_date": new_date}
    
    # Simulate updating a shipped order (should not be allowed)
    result = update_delivery_date(123, "2024-12-31")
    print(f"Updated shipped order: {result}")
    return True

def test_weak_crypto():
    """Test weak cryptography"""
    print("Testing weak cryptography...")
    import hashlib
    
    password = "mypassword123"
    weak_hash = hashlib.md5(password.encode()).hexdigest()
    print(f"MD5 hash of password: {weak_hash}")
    return True

def main():
    """Run all vulnerability tests"""
    print("=" * 60)
    print("Security Vulnerability Demo - Test Script")
    print("=" * 60)
    print()
    
    tests = [
        ("Command Injection", test_command_injection),
        ("SQL Injection", test_sql_injection),
        ("Insecure Deserialization", test_insecure_deserialization),
        ("Hardcoded Secrets", test_hardcoded_secrets),
        ("Business Logic Flaw", test_business_logic_flaw),
        ("Weak Cryptography", test_weak_crypto),
    ]
    
    for test_name, test_func in tests:
        print(f"\n🔍 {test_name}")
        print("-" * 40)
        try:
            test_func()
            print(f"✅ {test_name} test completed")
        except Exception as e:
            print(f"❌ {test_name} test failed: {e}")
    
    print("\n" + "=" * 60)
    print("All tests completed!")
    print("These vulnerabilities should be detected by Amazon Inspector.")
    print("=" * 60)

if __name__ == "__main__":
    main()