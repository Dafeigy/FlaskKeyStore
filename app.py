from flask import Flask, request, abort, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# 预定义的用户和密码哈希
USERS = {
    'silicon':"scrypt:32768:8:1$f7IzzH4trTjQ7hMm$4cf52593bb7226690015c7304489544271aec2ab8c1a0213a8a6534fa7d236e9aca7207daefd60071a1262c8cb0d540ce0b4268eed291a27434d143f3d6a8f74",
    'continue': "scrypt:32768:8:1$scBnHhjeVhACqKmO$1c3831fa60c3c9154f2fea1ecefb95943cbfda5ee95e4e5bd465379fa39398a80ca3446cb1cfe577042bc20c7d7b27d38687a7201efc490d2e6889da490e51e8"
}
print(generate_password_hash('ccr24202'))
@app.route('/login', methods=['GET'])
def protected():
    auth = request.authorization
    if not auth or not check_auth(auth.username, auth.password):
        abort(401, description="Unauthorized: Bad credentials")
    return jsonify({'message': 'You are authenticated!'})

def check_auth(username, password):
    stored_password_hash = USERS.get(username)
    if stored_password_hash:
        return check_password_hash(stored_password_hash, password)
    return False

if __name__ == '__main__':
    app.run(debug=True, port=5000)