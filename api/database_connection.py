import os
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker, Session
from users.model import Base, Users, User_requests 
from datetime import datetime, timedelta
from dataclasses import dataclass

from atp_users_hkls import users_hkls

#postgress
DATABASE_URL = os.getenv("DATABASE_URL")
CHAT_ID_KIRA = os.getenv("CHAT_ID_KIRA")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base.metadata.create_all(engine)

session1 = SessionLocal()

person_list = []
for user in users_hkls:
    
    user_current = Users(id = user['id'], 
                         name = user['name'], 
                         group = user['group'], 
                         surname = user['surname'], 
                         email = user['email'], 
                         chat_id = user['chat_id'], 
                         GRL = user['GRL'], 
                         level = user['level'], 
                         city = user['city'], 
                         chat_id_grl = user['chat_id_grl'])
    
    person_list.append(user_current)

with session1:

    for person in person_list:

        stmt = select(Users).where(Users.id == person.id)
        user = session1.execute(stmt).scalars().first()

        if user is None:

            session1.add_all([person])
            session1.commit()


with session1:

    stmt = select(Users).where(Users.id == "TEST")
    user = session1.execute(stmt).scalars().first()
    
    if user is not None:

        new_status = User_requests(
            work_status = "Remote",
            user_id = user.id,
            date_message = datetime.now(),
            date_for_request = datetime.now() + timedelta(days=1),
            message = "hello, i'm sick", 
            user=user,
            approve_grl=False
            )

        session1.add_all([new_status])
        session1.commit()





        

