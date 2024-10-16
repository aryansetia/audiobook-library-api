from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse
from src.models.user_account import User
from src.schemas.authentication import Token, LoginRequest
from src.schemas.user_account import UserCreate, UserUpdate, UserResponse
from src.database import get_db
from sqlalchemy.exc import IntegrityError
from passlib.context import CryptContext
from src.authentication.auth import get_password_hash
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from src.authentication.auth import authenticate_user, create_access_token

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/token")
def login_for_access_token(login_request: LoginRequest, db: Session = Depends(get_db)
                           ):
    user = authenticate_user(db, login_request.username, login_request.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/users/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        password_hash=hashed_password
    )

    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": "User has been registered."})
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists.")


@router.get("/users/{id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def get_user(id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == id).first()

    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")

    return db_user


@router.put("/users/{id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def update_user(id: int, user: UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == id).first()

    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")

    update_data = user.model_dump(exclude=("password",), exclude_unset=True)

    try:
        for key, value in update_data.items():
            setattr(db_user, key, value)

        db.commit()
        return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "User has been updated."})
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL, detail=str(e))


@router.delete("/users/{id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def delete_user(id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == id).first()

    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")

    try:
        db.delete(db_user)
        db.commit()
        return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "User has been deleted."})
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
