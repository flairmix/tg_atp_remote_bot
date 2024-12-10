from litestar import Controller, get, post, put, patch, delete, Request, Response
from litestar.dto import DTOData
from typing import Generator
from data.database_connection import SessionLocal

from data.users.model import User, Status
from sqlalchemy.orm import Session
from sqlalchemy import text, select

# Dependency to provide a database session
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class UserController(Controller):
    path = "/users"
    tags=["users"]

    # @get("/")
    # async def list_users(self) -> list[User]: ...

    @get("/")
    async def hello_world(self) -> dict[str, str]:
        """Handler function that returns a greeting dictionary."""
        return {"hello": "world"}
    

    @get("/{input_name:str}", dependencies={"db": get_db})
    async def user(self, db: Session, input_name:str) -> dict:
        """docs"""
        stmt = select(User).where(User.shortname == input_name)
        user = db.execute(stmt).scalars().first()

        return {
            "id" : user.id, 
            "shortname" : user.shortname, 
            "fullname" : user.fullname, 
            "email" : user.email, 
            "group" : user.group, 
            "GRL" : user.GRL
            }
    

    data_user_example = {
        "shortname" : "MID",
        "fullname" : "Донченко Михаил Александрович",
        "email" : "michail.donchenko@atp-tlp.ru", 
        "group" : "HKLS",
        "GRL" : "KIRA"
    }


    @post("/create_user", dependencies={"db": get_db})
    async def create_user(self, 
                          db: Session, 
                          request: Request,
                          data:dict) -> None:
        """docs"""

        new_user = User(
            shortname = data.get('shortname'),
            fullname = data.get('fullname'),
            email = data.get('email'), 
            group = data.get('group'),
            GRL = data.get('GRL')
        )

        db.add_all([new_user])
        db.commit()



    @get("/all", dependencies={"db": get_db})
    async def list_users(self, db: Session) -> dict:
        """docs"""
        stmt = select(User)
        users = db.execute(stmt).scalars().all()

        result = []

        for user in users:
            result.append(
                {
                "id" : user.id, 
                "shortname" : user.shortname, 
                "fullname" : user.fullname, 
                "email" : user.email, 
                "group" : user.group, 
                "GRL" : user.GRL
                }
            )

        return result