import os
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker, Session
from data.users.model import Base, User, Status 
from datetime import datetime, timedelta

#sqlite
# engine = create_engine("sqlite:///tutorial.db", echo=True)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


#postgress
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base.metadata.create_all(engine)

session1 = SessionLocal()

#test fill db 
with session1:

    stmt = select(User).where(User.shortname == "TEST")
    user = session1.execute(stmt).scalars().first()

    if user is None:
        current_user = User(
            shortname = "TEST",
            fullname = "TEST Михаил Александрович",
            email = "TEST.donchenko@atp-tlp.ru", 
            group = "HKLS",
            GRL = "KIRA"
        )

        session1.add_all([current_user])
        session1.commit()

        new_status = Status(
            work_status = "Remote",
            user_id = current_user.id,
            date_message = datetime.now(),
            date_for_request = datetime.now() + timedelta(days=1),
            message = "hello, i'm sick"
            )

        session1.add_all([new_status])
        session1.commit()
