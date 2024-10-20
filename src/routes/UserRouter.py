from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.database import get_async_session
from src.database.schemas.UserSchemas import SUserAuth, SUserResponse
from src.services.UserService import UserService, get_user_service
from src.utils.TokenService import TokenService

user_router = APIRouter(prefix='/users', tags=['Users'])


@user_router.post('/register')
async def register_user(
    response: Response,
    user_request: SUserAuth = Depends(SUserAuth),
    user_service: UserService = Depends(get_user_service),
    session: AsyncSession = Depends(get_async_session),
) -> SUserResponse:
    user: SUserResponse = await user_service.register(user_request, session)

    token = TokenService.create_token(
        payload={'sub': str(user.id), 'email': user.email}
    )

    response.set_cookie(
        'auth_token', token, secure=True, httponly=True, samesite='strict'
    )

    return user


@user_router.post('/login')
async def login_user(
    response: Response,
    user_request: SUserAuth = Depends(SUserAuth),
    user_service: UserService = Depends(get_user_service),
    session: AsyncSession = Depends(get_async_session),
) -> SUserResponse:
    user: SUserResponse = await user_service.login(user_request, session)

    token = TokenService.create_token(
        payload={'sub': str(user.id), 'email': user.email}
    )

    response.set_cookie(
        'auth_token', token, secure=True, httponly=True, samesite='strict'
    )

    return user


@user_router.post('/logout')
async def logout_user(response: Response):
    response.delete_cookie('auth_token')
    return True
