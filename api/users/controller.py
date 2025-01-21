from datetime import datetime
from litestar import Controller, get, post, put, patch, delete, Request, Response
from litestar.dto import DTOData
from typing import Generator
from database_connection import SessionLocal
import uuid

from users.model import Users, User_requests
from sqlalchemy.orm import Session
from sqlalchemy import text, select, update
from sqlalchemy.exc import SQLAlchemyError


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
  

    @get("/{id:str}", dependencies={"db": get_db})
    async def user(self, db: Session, id:str) -> dict | Response:
        """
        Get detailed information about a specific user based on their id.

        Parameters:
        - `db`: Database session dependency.
        - `id`: Shortname of the user to retrieve.

        Returns:
        - If successful, returns a dictionary containing user details.
        - If unsuccessful, returns an HTTP response indicating that the user was not found.

        Raises:
        - Any exceptions raised by the database operations will be propagated to the caller.
        """

        stmt = select(Users).where(Users.id == id)
        user = db.execute(stmt).scalars().first()

        if user is not None:
            return {
                "id" : user.id, 
                "name" : user.name, 
                "surname" : user.surname, 
                "email" : user.email, 
                "group" : user.group, 
                "GRL" : user.GRL
                }
        else:
            return Response(content=None, 
                            status_code=204
                            )
    

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
        
        stmt = select(Users).where(Users.id == data.get('id'))
        user = db.execute(stmt).scalars().first()

        if user is None:
            new_user = Users(
                id = data.get('id'),
                name = data.get('name'),
                surname = data.get('surname'),
                email = data.get('email'), 
                level = data.get('level'), 
                city = data.get('city'), 
                group = data.get('group'),
                GRL = data.get('GRL'),
                chat_id = 0
            )

            db.add_all([new_user])
            db.commit()

            return Response(status_code=201, 
                            content=f"Users with id <{data.get('id')}> - created")
        else:
            return Response(status_code=409, 
                            content=
                            f"Users with id <{data.get('id')}> - already exist")
        

    @post("/create_user_request/{user_id:str}", dependencies={"db": get_db})
    async def create_user_request(self, 
                          db: Session, 
                          data:dict, 
                          user_id:str) -> Response:
        

        stmt = select(Users).where(Users.id == user_id)
        user_db = db.execute(stmt).scalars().first()
        
        if user_db is not None:
            new_user_request = User_requests(
                work_status = data.get('work_status'),
                date_message = datetime.now(),
                message= data.get('message'),
                date_for_request = data.get('date_for_request'),
                user_id = data.get('id'),
                user = user_db,
                approve_grl=False
            )

            db.add_all([new_user_request])
            db.commit()

            return Response(status_code=201, 
                            content=f"User_request with id <{user_id}> - created")
        else:
            return Response(status_code=409, 
                            content=
                            f"Error with creating user_request")


    @get("/list_users", dependencies={"db": get_db})
    async def list_users(self, db: Session) -> list:
        """
        Retrieve a list of all users from the database.
        
        Parameters:
        - `db`: Database session dependency.
        
        Returns:
        - A dictionary containing a list of all users with their details.
        
        Raises:
        - Any exceptions raised by the database operations will be propagated to the caller.
        """

        stmt = select(Users)
        users = db.execute(stmt).scalars().all()

        result = []

        for user in users:
            result.append(
                {
                "id" : user.id, 
                "name" : user.name, 
                "surname" : user.surname, 
                "email" : user.email, 
                "group" : user.group, 
                "GRL" : user.GRL,
                "city" : user.city,
                }
            )

        return result
    
    @get("/list_user_requests/{id:str}", dependencies={"db": get_db})
    async def list_user_requests(self, 
                                 db: Session, 
                                 id:str) -> list:

        stmt = select(User_requests).where(User_requests.user_id == id)
        user_requests = db.execute(stmt).scalars().all()

        result = []

        for request in user_requests:
            result.append(
                {
                "id" : request.id, 
                "work_status" : request.work_status, 
                "user_id" : request.user_id, 
                "date_for_request" : request.date_for_request, 
                "message" : request.message, 
                "date_message" : request.date_message,
                "approve_grl" : request.approve_grl
                }
            )

        return result

    @put(path="approve_request_by_grl/{request_id:uuid}", dependencies={"db": get_db})
    async def approve_request_by_grl(self, db: Session, request_id:uuid.UUID) -> None:

        try:
            db.execute(update(User_requests).where(User_requests.id == request_id).values(approve_grl=True))
            db.commit()
            
            return Response(status_code=200, content=f"Request {request_id} approved successfully.")
        
        except SQLAlchemyError as e:
            db.rollback()
            return Response(status_code=500, content=f"Internal Server Error: {e}")
        
        except Exception as e:
            db.rollback()
            return Response(status_code=400, content=f"Bad Request: {e}")

    @delete("/delete_user/{id:str}", dependencies={"db": get_db})
    async def delete_user(self, db: Session, id:str) -> None:
        """Deletes a user by their id.

        Arguments:
        - db (Session): Database session.
        - id (str): The user's id.

        Returns:
        - Response: A response with the corresponding status and content.

        Status codes:
        - 200: Users successfully deleted.
        - 204: Users with the specified id was not found.
        """

        stmt = select(Users).where(Users.id == id)
        user = db.execute(stmt).scalars().first()

        if user is not None:
            db.delete(user)
            db.commit()

            return Response(status_code=200, 
                            content=f"User <{id}> deleted")
        else:
            return Response(status_code=204,
                            content=f"Users <{id}> not found")
                            
