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
2. Build the docker image
```bash
docker build -t my-fastapi-app .

```
3. Run the docker container 
```bash
docker run -d -p 8000:8000 --name my-fastapi-container my-fastapi-app
```
4. The FastAPI server will be running on `http://localhost:8000`
5. Go to `localhost:8000/users/register` and register yourself with username and password. 
6. Now go to `localhost:8000/token` and enter your credentials to get the access token.
7. Pass this token in the Authorization header as a Bearer token to access the protected routes.   

## API Documentation
The API documentation can be accessed at `http://localhost:8000/docs`

