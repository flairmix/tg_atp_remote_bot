from litestar import Controller, get, post, put, patch, delete, Request, Response
from litestar.dto import DTOData
from typing import Generator
from database_connection import SessionLocal

from users.model import User, Status
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
  

    @get("/{shortname:str}", dependencies={"db": get_db})
    async def user(self, db: Session, shortname:str) -> dict | Response:
        """
        Get detailed information about a specific user based on their shortname.

        Parameters:
        - `db`: Database session dependency.
        - `shortname`: Shortname of the user to retrieve.

        Returns:
        - If successful, returns a dictionary containing user details.
        - If unsuccessful, returns an HTTP response indicating that the user was not found.

        Raises:
        - Any exceptions raised by the database operations will be propagated to the caller.
        """

        stmt = select(User).where(User.shortname == shortname)
        user = db.execute(stmt).scalars().first()

        if user is not None:
            return {
                "id" : user.id, 
                "shortname" : user.shortname, 
                "fullname" : user.fullname, 
                "email" : user.email, 
                "group" : user.group, 
                "GRL" : user.GRL
                }
        else:
            return Response(status_code=404, 
                            content=f"User with shortname <{shortname}> - not found")
    

    @post("/create_user", dependencies={"db": get_db})
    async def create_user(self, 
                          db: Session, 
                          data:dict) -> Response:
        """
        Create a new user in the database.
        
        Parameters:
        - `db`: Database session dependency.
        - `data`: Dictionary containing user information.
        
        Returns:
        - If successful, returns a response indicating that the user was created.
        - If unsuccessful, returns a response indicating that the user already exists.
        
        Raises:
        - Any exceptions raised by the database operations will be propagated to the caller.
        """
        
        stmt = select(User).where(User.shortname == data.get('shortname'))
        user = db.execute(stmt).scalars().first()

        if user is None:
            new_user = User(
                shortname = data.get('shortname'),
                fullname = data.get('fullname'),
                email = data.get('email'), 
                group = data.get('group'),
                GRL = data.get('GRL')
            )

            db.add_all([new_user])
            db.commit()

            return Response(status_code=201, 
                            content=f"User with shortname <{data.get('shortname')}> - created")
        else:
            return Response(status_code=409, 
                            content=
                            f"User with shortname <{data.get('shortname')}> - already exist")



    @get("/list_users", dependencies={"db": get_db})
    async def list_users(self, db: Session) -> dict:
        """
        Retrieve a list of all users from the database.
        
        Parameters:
        - `db`: Database session dependency.
        
        Returns:
        - A dictionary containing a list of all users with their details.
        
        Raises:
        - Any exceptions raised by the database operations will be propagated to the caller.
        """

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
                "GRL" : user.GRL,
                "city" : user.city,
                }
            )

        return result
    

    @delete("/delete_user/{shortname:str}", dependencies={"db": get_db})
    async def delete_user(self, db: Session, shortname:str) -> None:
        """Deletes a user by their shortname.

        Arguments:
        - db (Session): Database session.
        - shortname (str): The user's shortname.

        Returns:
        - Response: A response with the corresponding status and content.

        Status codes:
        - 200: User successfully deleted.
        - 404: User with the specified shortname was not found.
        """

        stmt = select(User).where(User.shortname == shortname)
        user = db.execute(stmt).scalars().first()

        if user is not None:
            db.delete(user)
            db.commit()

            return Response(status_code=200)
        else:
            return Response(status_code=404,
                            content=f"User <{shortname}> not found")
                            
