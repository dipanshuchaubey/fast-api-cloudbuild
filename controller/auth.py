import jwt


def get_jwt(data: dict, secret: str):
    return jwt.encode(data, secret, algorithm="HS256")


def decode_jwt(token: str, secret: str):
    return jwt.decode(token, secret, algorithms=["HS256"])
