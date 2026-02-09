from fastapi import FastAPI

from src.myapp.interfaces import api


def create_app():
    myapp = FastAPI()
    myapp.include_router(api.router)
    return myapp


app = create_app()
