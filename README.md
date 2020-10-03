# User  

## User Frontend:
 - Note: "Action" attribute in both login and signup has to be either `login` or `register`
### Login
- Request method type: POST      
 ```
 {
     "Action" : "login",
     "Username": "{username}",
     "Password": "{password}",
 }
 ```
- Response: will be: 
```
{
    'statusCode': 200,
    'Status': true or false,
    'Token': token or None,
    'Error': None or errorMessage
}
```

### Signup
- Request method type: POST         
 ```
 {
     "Action" : "register",
     "Username": "{username}",
     "Password": "{password}",
     "Email": "{email}",
     "FirstName": "{firstname}",
     "LastName": "{lastname}",
     "Country": "{country}",
     "City": "{city}"
 }
 ```
 - Response: will be: 
```
{
    'statusCode': 200,
    'Status': true or false,
    'Error': None or errorMessage
}
```

## User Service Backend

### Login
 - Your RESTapi with route `/login` will receive a json formated POST request like this       
 ```
 {
   "Username": "{username}",
   "Password": "{password}"
 }
 ```
   Please verify the password with db, then the expected return should be in dict, template shown below:
 ```
 {
   "Result": True or False   
 }
 ```        
   Note: True means verfied, False means either account error or password error.

### Register
 - for register, your RESTapi with route "/register" you will receive a json formated POST request like this              
 ```
 {
   "Username": "{username}",
   "Password": "{password}",
   "Email": "{email}",
   "FirstName": "{firstname}",
   "LastName": "{lastname}",
   "Country": "{country}",
   "City": "{city}"   
 }          
 ```
   Please store in database, then expected return should be in dict, template shown below:          
 ```    
 {
   "Result": True or False  
 }
 ```            
   Note: True means sucessfully signed up, False means something is wrong
