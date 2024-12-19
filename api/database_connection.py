import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker, Session
from users.model import Base, User, Status 
from datetime import datetime, timedelta

# current_dir = os.path.abspath(os.path.dirname(__file__))
# parent_dir = os.path.dirname(current_dir)
# db_file = os.path.join(parent_dir, "tutorial.db")

#sqlite
# engine = create_engine("sqlite:///tutorial.db", echo=True)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


load_dotenv()
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
            shortname = "TEST_BE",
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
