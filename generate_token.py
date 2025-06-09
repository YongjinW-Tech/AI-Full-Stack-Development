import random
import string

def generate_token():
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for i in range(16))

token = generate_token()
print(f"Jupyter Lab access token: {token}")