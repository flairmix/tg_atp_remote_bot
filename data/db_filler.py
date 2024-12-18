from .database_connection import SessionLocal
from sqlalchemy import select
from data.users.model import User, Status 
from datetime import datetime, timedelta


session = SessionLocal()

#fill db 
with session:


    stmt = select(User).where(User.shortname == "TEST")
    user = session.execute(stmt).scalars().first()

    if user is None:
        current_user = User(
            shortname = "TEST",
            fullname = "TEST Михаил Александрович",
            email = "TEST.donchenko@atp-tlp.ru", 
            group = "HKLS",
            GRL = "KIRA"
        )

        session.add_all([current_user])
        session.commit()

        new_status = Status(
            work_status = "Remote",
            user_id = current_user.id,
            date_message = datetime.now(),
            date_for_request = datetime.now() + timedelta(days=1),
            message = "hello, i'm sick"
            )

        session.add_all([new_status])
        session.commit()
