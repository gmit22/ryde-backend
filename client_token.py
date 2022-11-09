import jwt
from datetime import datetime, timedelta

#secret key used for encoding data
SECRET_KEY="hashencodetoken"
#encryption algorithm
ALGORITHM = "HS256"

def create_access_token(data: dict):
    to_encode = data.copy()
     
    # expire time of the token
    expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(payload=to_encode, key=SECRET_KEY, algorithm=ALGORITHM) 
    # return the generated token
    return encoded_jwt, expire
 
def get_token():
   
    # data to be signed using token
    data = {
        "user": "gunit",
        'authorised': True
    }
    token, expire = create_access_token(data=data)
    return {'token': token}, expire

if __name__ == "__main__":

    token, expiry_date = get_token()
    print(f"Generated token for future requests: {token} valid till {expiry_date}")
