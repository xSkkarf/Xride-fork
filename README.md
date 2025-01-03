# XDrive Car Rental API

### Clone the repository
```bash
git clone https://github.com/Macarious-GK/Xride.git
cd Xride

```
## Setup Instructions
### Set up a virtual environment
```bash
python -m venv env
source env/bin/activate  # For macOS/Linux
env\Scripts\activate  # For Windows
pip install -r requirements.txt


```
### Run the server
```python
python manage.py migrate
python manage.py runserver

```

### Admin User Creds: 
- Name: admin
- Password: admin

## End Points with JWT

### Authentication
Obtain a JWT Token through this API and the body of user and Password
- POST /token/

### APP: ride_V0
- GET V0/cars/ — List all cars.
- POST V0/cars/ — Create a new car.
- GET V0/cars/{id}/ — Retrieve a specific car.
- PUT V0/cars/{id}/ — Update a car.
- DELETE V0/cars/{id}/ — Delete a car.
- Authorization: Bearer your_access_token_here

### APP: ride_V1

- GET V1/cars/nearby-available/ — Get nearest available cars based on the user's latitude and longitude. "Nearest cars in N KM radius"
- POST V1/car/<int:car_id>/reserve/ — Reserve a specific car by its ID.
- POST V1/car/<int:car_id>/release/ — Release a reserved car, making it available again.
- POST V1/car/<int:car_id>/door-status/ — Change the door status of a specific car (open or close).
- Authorization: Bearer your_access_token_here

### APP: ride_V2

- GET V2/cars/<int:car_id>/status/ — Get the current readings for the specified car, including its temperature and door status.
- POST V2/car/<int:car_id>/update-door/ — Update the door status of a specific car (lock or unlock). Body -> {"action": "unlock"}
- POST V2/car/<int:car_id>/update-gas/ — Update the gas status for a specific car (if applicable). Body -> {"gas": 100 }
- POST V2/car/<int:car_id>/update-temperature/ — Update the temperature of a specific car. Body -> {"temperature": 26 }.
- Authorization: Bearer your_access_token_here

### APP: ride_V3

#### Car Endpoints:

- GET V3/car/nearby-available/ — Get a list of cars available within a specified radius.
- POST V3/car/<int:car_id>/reserve/ — Reserve a specified car if available and user has sufficient balance. Body:{"reservation_plan": "2H" // or "6H", "12H"}
- POST V3/car/<int:car_id>/release/ — Release a car that has been reserved, marking it as available for others.
- GET V3/car/<int:car_id>/status/ — Get the current status of the specified car, including attributes like temperature, door status, and gas level.
- POST V3/car/<int:car_id>/update-door/ — Update the door status of a specific car (lock or unlock).Body:{  "action": "unlock" // or "lock"}
#### User Endpoints:

- GET V3/user/profile/ — Retrieve the profile details of the authenticated user.
- GET V3/user/trips/ — List all reservations or trips made by the user, including past and active ones.

#### Payment Endpoints:

- POST V3/user/payments/create/ — Initiate a payment process for reserving a car.
- POST V3/user/payments/confirm/ — Confirm a payment transaction after it’s been initiated.
- POST V3/user/payments-HMAC/confirm/ — Confirm a payment using HMAC verification.

######

# Frontend APIs

- /users/
- /users/me/
- /users/resend_activation/
- /users/set_password/
- /users/reset_password/
- /users/reset_password_confirm/

# Backend APIs

- /auth/activate/<str:uid>/<str:token>/

- /users/activation/
data = {
    'uid': uid,
    'token': token
        }

- /auth/password/reset/confirm/<str:uid>/<str:token>/

- /users/reset_password_confirm/
data = {
    "uid": "",
    "token": "",
    "new_password": "",
    "re_new_password": ""
}

# APIS

## API to create user 
POST /users/
{
    "username": "",
    "email": "",
    "first_name": "",
    "last_name": "",
    "phone_number": "",
    "address": "",
    "national_id": "",
    "password": "",
    "re_password": "",
}

- Then an activation link will be sent to the user's email, after clicking on it the user account is activated
- The server send link activation email and success activation email

## API to Retrive user 
POST-PUT-DELETE /users/me/

Header ["Authorization": "JWT Token"]
- Use this endpoint to retrieve/update
- Used to delete User, require current_password in the DELETE request

## API to resend_activation Email
POST /users/resend_activation/

{
    "email": "",
}

- This resend activation email if the user in not active and the email is in use.
- The server send link activation email and success activation email
- Return Bad Request if the user is Active or the email is not registered

## API to activate user 
GET /auth/activate/<str:uid>/<str:token>/
POST /users/activation/

- These apis are for server use to get the uid and token to activate the user, frist api is sent to the user and by clicking the backend make a POST request api "/users/activation/" with data contain uid & token

## API to Set Password
POST /users/set_password/
Header ["Authorization": "JWT Token"]
body:
{
    "new_password":"",
    "re_new_password":"",
    "current_password":""
}
- Use this endpoint to change user password

## API to Reset Password (NEED WORK WITH FRONTEND)
POST /users/reset_password/
body:
{
    "email":"",
}
GET or POST /auth/password/reset/confirm/<str:uid>/<str:token>/ "UNDER WORK"
POST /users/reset_password_confirm/

- the first API take email and send a link to user email to reset the password.
- Then user use the second API "GET Request" this used by frontend to send a POST request to the thired API with this data:

data = {
    "uid": "",
    "token": "",
    "new_password": "",
    "re_new_password": ""
}


## API JWT Token Authentication
- /jwt/create/
body:
{
    "username": "",
    "password": ""
}
- /jwt/refresh/
body:
{
    "refresh": "refresh_Token",
}
- /jwt/verify/
body:
{
	"token": ""
}