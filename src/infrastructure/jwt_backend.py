from typing import Any, Dict, Optional
from jam.ext.fastapi import JWTBackend
from src.settings import settings
from src.infrastructure.jaminstance import jam

jwt_backend = JWTBackend(settings.JAM_SETTINGS, header_name="Authorization")


def make_access_token(payload: Dict[str, Any], exp: Optional[int] = None) -> str:
    """
    Создаёт JWT через Jam. Если exp=None — берётся дефолт из конфигурации Jam.
    """
    if exp is None:
        exp = settings.JAM_SETTINGS.get("jwt", {}).get("expire", 3600)
    p = jam.jwt_make_payload(exp, payload)
    return jam.jwt_create(p)


def verify_token(token: str, *, check_exp: bool = True) -> Dict[str, Any]:
    """
    Проверяет JWT и возвращает payload.
    """
    try:
        payload = jam.jwt_decode(token=token, check_exp=check_exp, check_list=False)
        print(f"DEBUG: Token verified. Payload: {payload}")
        return payload
    except Exception as e:
        print(f"DEBUG: Token verification failed: {e}")
        raise e
