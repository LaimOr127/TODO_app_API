from multiprocessing import get_context
from jose import JWTError, jwt
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from . import schemas, crud
from .database import get_db

# Конфигурация для JWT
SECRET_KEY = "your_secret_key" # Секретный ключ для подписи JWT
ALGORITHM = "HS256" # Алгоритм для подписи JWT
ACCESS_TOKEN_EXPIRE_MINUTES = 30 # Время жизни токена доступа (в минутах)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_access_token(data: dict, expires_delta: timedelta = None): # Функция для создания JWT токена
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def authenticate_user(db: Session, username: str, password: str): # Функция для аутентификации пользователя
    user = crud.get_user_by_username(db, username)
    if not user:
        return False
    if not get_context.verify(password, user.hashed_password):
        return False
    return user # Возвращаем пользователя, если аутентификация прошла успешно

def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)): # Функция для получения текущего пользователя из токена
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    ) # Исключение для невалидных учетных данных
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = crud.get_user_by_username(db, username)
    if user is None:
        raise credentials_exception
    return user
