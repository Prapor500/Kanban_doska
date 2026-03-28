from typing import Any, Dict, Optional
from jam.ext.fastapi import JWTBackend
from src.infrastructure.jaminstance import jam

jwt_backend = JWTBackend(jam)


def make_access_token(payload: Dict[str, Any], exp: Optional[int] = None) -> str:
    """
    Создаёт JWT через Jam. Если exp=None — берётся дефолт из конфигурации Jam.
    """
    p = jam.make_payload(exp=exp, **payload)
    return jam.gen_jwt_token(p)


def verify_token(token: str, *, check_exp: bool = True) -> Dict[str, Any]:
    """
    Проверяет JWT и возвращает payload.
    """
    return jam.verify_jwt_token(token=token, check_exp=check_exp, check_list=False)
