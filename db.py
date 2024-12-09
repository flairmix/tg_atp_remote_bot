import sqlite3
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker, Session
from model import Base, User, Status 
from datetime import datetime

engine = create_engine("sqlite:///tutorial.db", echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(engine)

session1 = SessionLocal()

with session1: 
    current_user = User(
        shortname = "MID",
        fullname = "Донченко Михаил Александрович",
        email_address = "michail.donchenko@atp-tlp.ru", 
        group = "HKLS",
        GRL = "KIRA"
    )

    session1.add_all([current_user])
    session1.commit()

    new_status = Status(
        work_status = "Remote",
        user_id = current_user.id,
        date_status = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )

    session1.add_all([new_status])
    session1.commit()





# session = Session(engine)
# stmt = select(User).where(User.name.in_(["spongebob", "sandy"]))
# for user in session.scalars(stmt):
#     print(user)
              


