from infrastructure.jaminstance import jam
from jam.exceptions import TokenLifeTimeExpired


def get_access_token(user_id):
    payload = jam.make_payload(exp=600, **{"user_id": user_id})
    token = jam.gen_jwt_token(payload)
    return token


def get_refresh_token(user_id):
    payload = jam.make_payload(**{"user_id": user_id})
    token = jam.gen_jwt_token(payload)
    return token


def get_check_token(token):
    try:
        jam.verify_jwt_token(
            token=token,
            check_exp=True,
            check_list=False
        )
    except TokenLifeTimeExpired:
        return False
    except ValueError:
        return False
    return True
