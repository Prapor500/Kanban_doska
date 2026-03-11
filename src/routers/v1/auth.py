from fastapi import APIRouter

auth = APIRouter(prefix="/auth")


@auth.post("log_in")
def log_in(email, password):
