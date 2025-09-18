from typing import Callable, Any
from fastapi import FastAPI, APIRouter

from app.infrastructure.db import Database, default_db
from app.interfaces import api


# class FastApi(Starlette):
#     def __init__(self, version: str = "0.1.0") -> None:
#         super().__init__()
#         self.version = version
#         self.router: APIRouter = APIRouter()
#
#     def get(
#         self,
#         path: str,
#     ) -> Callable[..., Any]:
#         return self.router.get(path)
#
#     def post(
#         self,
#         path: str,
#     ) -> Callable[..., Any]:
#         return self.router.post(path)
#
#     async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
#         await super().__call__(scope, receive, send)


def create_app():
    app = FastAPI()
    app.include_router(api.router)
    return app


app = create_app()
