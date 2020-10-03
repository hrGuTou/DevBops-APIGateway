import json
import jwt
import datetime
import requests

# endpoint = "User service REST api address"


########
# User Frontend:
#  - for login, method type: POST
# {
#     "Action" : "login",
#     "Username": "{username}",
#     "Password": "{password}",
# }
    # - response:
    #     {
    #         'statusCode': 200,
    #         'Status': true or false,
    #         'Token': token or None,
    #         'Error': None or errorMessage
    #     }

#  - for signup, method type: POST
# {
#     "Action" : "register",
#     "Username": "{username}",
#     "Password": "{password}",
#     "Email": "{email}",
#     "FirstName": "{firstname}",
#     "LastName": "{lastname}",
#     "Country": "{country}",
#     "City": "{city}"
# }
    # - response:
    #     {
    #         'statusCode':200,
    #         'Status': true or false,
    #         'Error': None or errorMessage
    #     }
########    
    
    
#########
# User Service backend:
# - for login, your RESTapi with route "/login" will receive a json formated POST request like this
# {
#   "Username": "{username}",
#   "Password": "{password}"
# }
# 
#   Please verify the password with db, then the expected return should be in dict, template shown below:
# {
#   "Result": True or False   
# }
#   Note: True means verfied, False means either account error or password error.

# - for register, your RESTapi with route "/register" you will receive a json formated POST request like this
# {
#   "Username": "{username}",
#   "Password": "{password}",
#   "Email": "{email}",
#   "FirstName": "{firstname}",
#   "LastName": "{lastname}",
#   "Country": "{country}",
#   "City": "{city}"   
# }
#
#   Please store in database, then expected return should be in dict, template shown below:
# {
#   "Result": True or False  
# }
#   Note: True means sucessfully signed up, False means something is wrong
########



headers = {
        "content_type": "application/json"
        }

endpoint = "https://822dc42d9945.ngrok.io"

def register(username, password, email, fname, lname, country, city):
    #return True or False
    
    data = {
         "Username": username,
         "Password": password,
         "Email": email,
         "FirstName": fname,
         "LastName": lname,
         "Country": country,
         "City": city
     }
    res = requests.post(endpoint+'/register', headers=headers, json=data).json()
    return res['Result']
    #return True
    
def login(username, password):
    #return True or False
    
    data = {
        "Username": username,
        "Password": password
    }
    res = requests.post(endpoint+'/login', headers=headers, json=data).json()
    
    return res['Result']


def lambda_handler(event, context):
    
    action = event['Action']
    
            
    if action == "register":
        username = event['Username']
        password = event['Password']
        email = event['Email']
        fname = event['FirstName']
        lname = event['LastName']
        country = event['Country']
        city = event['City']
        
        
        status = register(username, password, email, fname, lname, country, city)
        
        # User service should return either True on successfully created a user in db, or False if failed to do so
        # When saving user, the password should be hashed and avoid saving as plaintext. Ex: https://pypi.org/project/bcrypt/3.1.0/
        # OPTIONAL: User service should generate a UUID for each of the user as userID for primary key
        
        return {
            'statusCode':200,
            'Status': status,
            'Error': None
        }
        
    if action == "login":
        username = event['Username']
        password = event['Password']
        
        authen = login(username, password)
    
        # User service will verify the password in database, return True if verified, False if not. Suggestion: use bcrypt from above
        
        if(authen):
            # If verified, generate token
            token = encodeToken(username)
            if(token):
                return {
                    'statusCode': 200,
                    'Status': True,
                    'Token': token,
                    'Error': None,

                }
            else:
                return {
                    'statusCode': 200,
                    'Status': False,
                    'Token' : None,
                    'Error': 'Token generating error'
                }
        else:
            return {
                'statusCode': 200,
                'Status': False,
                'Token' : None,
                'Error': 'User authentication error'
            }
            
    return {
        'statusCode': 200,
        'Status': False,
        'Token' : None,
        'Error': "Action error"
    }
    

def encodeToken(username):
    try:
        payload={
            'Username': username,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
            'iat': datetime.datetime.utcnow()
        }
        
        return jwt.encode(
                payload,
                'devBopsSecret',
                algorithm='HS256'
            )
    except:
        return None