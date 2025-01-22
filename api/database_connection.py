import os
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker, Session
from users.model import Base, Users, User_requests 
from datetime import datetime, timedelta
from dataclasses import dataclass

from atp_users_hkls import users_hkls

#sqlite
# engine = create_engine("sqlite:///tutorial.db", echo=True)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

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

#testers db
# person_list = []

# user1 = Users(id = "TEST", name="TEST", surname="Donchenko", email="TEST.donchenko@atp-tlp.ru", 
#     group="DEV", chat_id=432923144, GRL="KIRA", level="TL2", city="MOS", chat_id_grl=CHAT_ID_KIRA)

# user1_1 = Users(id = "MID", name="Михаил", surname="Donchenko", email="TEST.donchenko@atp-tlp.ru", 
#     group="DEV", chat_id=432923144, GRL="KIRA", level="TL2", city="MOS", chat_id_grl=CHAT_ID_KIRA)

# user2 =  Users(id = "GUV", name="Vsevolod", surname="Gurov", email="Vsevolod.Gurov@atp-tlp.ru", 
#     group="BIM", chat_id=0, GRL="KIRA", level="TL1", city="MOS", chat_id_grl=CHAT_ID_KIRA)

# user3 = Users(id = "SHKA", name="Egor", surname="Shkaev", email="Egor.Shkaev@atp-tlp.ru", 
#     group="BIM", chat_id=0, GRL="KIRA", city="SPB", level="TL1", chat_id_grl=CHAT_ID_KIRA)

# user4 = Users(id = "INI", name="Nikita", surname="Ignatiev", email="Nikita.Ignatiev@atp-tlp.ru", 
#     group="OV", chat_id=0, GRL="KIRA", level="PRAK", city="MOS", chat_id_grl=CHAT_ID_KIRA)

# user5 = Users(id = "ADL", name="Alexander", surname="Dolinskiy", email="Alexander.Dolinskiy@atp-tlp.ru", 
#     group="OV", chat_id=0, GRL="KIRA", level="PRAK", city="MOS", chat_id_grl=CHAT_ID_KIRA)

# user6 = Users(id = "PDE", name="Fedor", surname="Perkhalyuk", email="Fedor.Perkhalyuk@atp-tlp.ru", 
#     group="VK", chat_id=0, GRL="KIRA", level="-", city="MOS", chat_id_grl=CHAT_ID_KIRA)

# user7 = Users(id = "VAN", name="Anastasia", surname="Volodina", email="Anastasia.Volodina@atp-tlp.ru", 
#     group="VK", chat_id=0, GRL="KIRA", level="-", city="MOS", chat_id_grl=CHAT_ID_KIRA)

# user8 = Users(id = "KIRA", name="Andrey", surname="Kirpichnikov", email="Andrey.Kirpichnikov@atp-tlp.ru", 
#     group="HKLS", chat_id=0, GRL="KIRA", level="GRL", city="MOS", chat_id_grl=CHAT_ID_KIRA)


# person_list.append(user1)
# person_list.append(user1_1)
# person_list.append(user2)
# person_list.append(user3)
# person_list.append(user4)
# person_list.append(user5)
# person_list.append(user6)
# person_list.append(user7)
# person_list.append(user8)


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





        

