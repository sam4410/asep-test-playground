JWT_SECRET = "your-secret-key"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

def sign_access_token(data: dict, expires_minutes: int = 15) -> str:
    """
    Create a signed JWT access token.
    The payload must contain at least a ``sub`` (subject) claim.
    ``exp`` is automatically added based on ``expires_minutes``.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, JWT_SECRET, algorithm=ALGORITHM)

def verify_access_token(token: str) -> dict:
    """
    Verify a JWT access token's signature and expiration.
    Returns the decoded payload if valid, otherwise raises HTTPException.
    """
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid access token",
            headers={"WWW-Authenticate": "Bearer"},
        )

def decode_jwt(token: str) -> dict:
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
def require_role(required_role: str) -> Callable:
    async def role_checker(token: str = Depends(oauth2_scheme)):
        return payload
    
    return role_checker

# Backward compatibility aliases (used in other modules)
sign_jwt = sign_access_token
verify_jwt = verify_access_token
