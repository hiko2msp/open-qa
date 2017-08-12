import os

import base64
import hmac
import hashlib

from flask import Flask

app = Flask(__name__)

# sha256_hash_digest = hmac.new()

@app.route('/')
def hello():
    return 'Hello World!' + str(os.environ.get('TEST', 'no test'))

if __name__ == '__main__':
    app.run()
