# Audiobook Managment System APIs using FastAPI and Sqlite3

## Overview
This repository contains the source code developed as an assignment for the SWE role at Senquire. The project focuses on integrating the Audiobook Management System APIs with FastAPI. 

## Tech Stack
The project utilizes the following technologies:

- FastAPI
- JWT for authentication
- SQLAlchemy
- Docker

## Setup 
To run this project, you need to have Docker and Docker Compose installed on your machine. 

1. Clone the repository
2. Create a .env file in the root directory with below variables
```bash 
SECRET_KEY="abcd"  # Replace this with a strong secret key
ALGORITHM=HS256  # This is typically the algorithm used for JWT
ACCESS_TOKEN_EXPIRE_MINUTES=30  # Token expiration time in minutes
```

3. Build the docker image
```bash
docker build -t my-fastapi-app .

```
4. Run the docker container 
```bash
docker run -d -p 8000:8000 --name my-fastapi-container my-fastapi-app
```
5. The FastAPI server will be running on `http://localhost:8000`
6. Go to `localhost:8000/users/register` and register yourself with username and password. 
7. Now go to `localhost:8000/token` and enter your credentials to get the access token.
8. Pass this token in the Authorization header as a Bearer token to access the protected routes.   

## Tests
To run the test cases, first create a virtual environment and install all the requirements using 
```bash
pip install -r requirements.txt
```
Use this command to run the test cases for audiobook APIs
```bash
pytest tests/test_audiobook.py
```
## API Documentation
The API documentation can be accessed at `http://localhost:8000/docs`

