import os
from flask import Flask
from flask import request
from flask import make_response
import db
app = Flask(__name__)

@app.route('/api/input', methods=['POST'])
def sample():
  name = request.form['name']
  return "name"


@app.route('/login', methods=['POST'])
def login():
  # get salt, name, and use hashlib to authenticate
  resp = make_response('')
  resp.set_cookie('ayobi_auth', "SAMPLE")
  return resp

@app.route('/signup', methods=['POST'])
def signup():
  createUser()

@app.route('/health')
def health():
  return "ALIVE"

if __name__ == "__main__":
  port = int(os.environ.get('PORT', 5000))
  app.run(host='0.0.0.0', port=port, debug=True)
