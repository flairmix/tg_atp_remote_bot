import os
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker, Session
from data.users.model import Base, User, Status 
from datetime import datetime, timedelta
from dataclasses import dataclass

#sqlite
# engine = create_engine("sqlite:///tutorial.db", echo=True)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#postgress
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base.metadata.create_all(engine)

session1 = SessionLocal()


#testers db
person_list = []

user1 = User(shortname = "TEST", fullname="TEST Михаил Александрович", email="TEST.donchenko@atp-tlp.ru", 
    group="DEV", chat_id=432923144, GRL="KIRA", level="TL2", city="MOS")

user2 =  User(shortname = "GUV", fullname="Gurov Vsevolod", email="Vsevolod.Gurov@atp-tlp.ru", 
    group="BIM", chat_id=0, GRL="KIRA", level="TL1", city="MOS")

user3 = User(shortname = "SHKA", fullname="Shkaev Egor", email="Egor.Shkaev@atp-tlp.ru", 
    group="BIM", chat_id=0, GRL="KIRA", city="SPB", level="TL1")

user4 = User(shortname = "INI", fullname="Ignatiev Nikita", email="Nikita.Ignatiev@atp-tlp.ru", 
    group="OV", chat_id=0, GRL="KIRA", level="PRAK", city="MOS")

user5 = User(shortname = "ADL", fullname="Dolinskiy Alexander", email="Alexander.Dolinskiy@atp-tlp.ru", 
    group="OV", chat_id=0, GRL="KIRA", level="PRAK", city="MOS")

user6 = User(shortname = "PDE", fullname="Perkhalyuk Fedor", email="Fedor.Perkhalyuk@atp-tlp.ru", 
    group="VK", chat_id=0, GRL="KIRA", level="-", city="MOS")

user7 = User(shortname = "VAN", fullname="Volodina Anastasia", email="Anastasia.Volodina@atp-tlp.ru", 
    group="VK", chat_id=0, GRL="KIRA", level="-", city="MOS")

user8 = User(shortname = "KIRA", fullname="Kirpichnikov Andrey", email="Andrey.Kirpichnikov@atp-tlp.ru", 
    group="HKLS", chat_id=0, GRL="KIRA", level="GRL", city="MOS")


person_list.append(user1)
person_list.append(user2)
person_list.append(user3)
person_list.append(user4)
person_list.append(user5)
person_list.append(user6)
person_list.append(user7)
person_list.append(user8)


with session1:

    for person in person_list:

        stmt = select(User).where(User.shortname == person.shortname)
        user = session1.execute(stmt).scalars().first()

        if user is None:

            session1.add_all([person])
            session1.commit()
        
        if  person.shortname == "TEST":
            new_status = Status(
                work_status = "Remote",
                user_id = user.id,
                date_message = datetime.now(),
                date_for_request = datetime.now() + timedelta(days=1),
                message = "hello, i'm sick", 
                user=user
                )

            session1.add_all([new_status])
            session1.commit()





        

