
Simple user database (in-memory)

users = {
    "admin": {
        "password": "admin123",
        "role": "admin"
    },
    "john": {
        "password": "user123",
        "role": "user"
    }
}


# Authentication function
def authenticate(username, password):
    if username in users and users[username]["password"] == password:
        return users[username]
    return None
