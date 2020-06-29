import config

from werkzeug.security import generate_password_hash, check_password_hash
from flask_httpauth import HTTPBasicAuth


auth = HTTPBasicAuth()

users = {
    config.username: generate_password_hash(config.password),
}

@auth.verify_password
def verify_password(username, password):
    if username in users and \
            check_password_hash(users.get(username), password):
        return username
