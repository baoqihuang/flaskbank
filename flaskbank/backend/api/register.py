from .. import all_module as am
from .utils import to_d128
register_bp = am.Blueprint('register', __name__)


@register_bp.route('/register', methods=['POST'])
def register_user():
    data = am.request.get_json()
    if not data:
        return am.jsonify({'msg': 'Bad Request, no data passed'}), 400

    try:
        first = data["first_name"]
        last = data["last_name"]
        email = data["email"]
        username = data["username"]
        password = data['password']
    except KeyError:
        return am.jsonify({'msg': 'Bad Request, missing/misspelled key'}), 400

    if not am.clients.find_one({"username": username}):
        am.clients.insert_one({
            'first_name': first,
            'last_name': last,
            'username': username,
            'email': email,
            'password': am.bcrypt.generate_password_hash(password.encode(
                'UTF-8')),

            'accounts': [
                {
                    'account_number': am.get_account_num('checking'),
                    'alias': 'Checking Account',
                    'balance': to_d128(0.0),
                    'type': 'checking',
                    'active': True,
                    'transactions': []
                },
                {
                    'account_number': am.get_account_num('saving'),
                    'alias': 'Saving Account',
                    'balance': to_d128(0.0),
                    'type': 'saving',
                    'active': True,
                    'transactions': []
                }
            ]
        })
        return am.jsonify({'msg': 'User Registered'}), 201

    return am.jsonify({'msg': 'Username already exist'}), 409
