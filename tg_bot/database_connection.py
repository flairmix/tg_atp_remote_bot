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

person_list = []

class Person():
    def __init__(self, 
            shortname:str, 
            fullname:str, 
            email:str, 
            level:str,  
            group="HKLS",
            chat_id=0, GRL="KIRA", city="MOS"):

        self.shortname = shortname
        self.fullname = fullname
        self.email = email
        self.group = group
        self.level = level
        self.chat_id = chat_id
        self.GRL = GRL
        self.city = city
        person_list.append(self)


Person(shortname = "TEST", fullname="TEST Михаил Александрович", email="TEST.donchenko@atp-tlp.ru", 
    group="DEV", chat_id=432923144, GRL="KIRA", level="TL2")

Person(shortname = "GUV", fullname="Gurov Vsevolod", email="Vsevolod.Gurov@atp-tlp.ru", 
    group="BIM", chat_id=0, GRL="KIRA", level="TL1")

Person(shortname = "SHKA", fullname="Shkaev Egor", email="Egor.Shkaev@atp-tlp.ru", 
    group="BIM", chat_id=0, GRL="KIRA", city="SPB", level="TL1")

Person(shortname = "INI", fullname="Ignatiev Nikita", email="Nikita.Ignatiev@atp-tlp.ru", 
    group="OV", chat_id=0, GRL="KIRA", level="PRAK")




with session1:

    for person in person_list:

        stmt = select(User).where(User.shortname == person.shortname)
        user = session1.execute(stmt).scalars().first()

        if user is None:
            current_user = User(
                shortname = person.shortname,
                fullname = person.fullname,
                email = person.email, 
                group = person.group,
                level = person.level,
                chat_id = person.chat_id,
                GRL = person.GRL,
                city = person.city
            )

            session1.add_all([current_user])
            session1.commit()
        
        if User.shortname == "TEST":
            new_status = Status(
                work_status = "Remote",
                user_id = current_user.id,
                date_message = datetime.now(),
                date_for_request = datetime.now() + timedelta(days=1),
                message = "hello, i'm sick"
                )

            session1.add_all([new_status])
            session1.commit()





        

# •	Gurov, Vsevolod            GUV      BIM       TL1         Gurov Vsevolod  Vsevolod.Gurov@atp-tlp.ru
# •	Shkaev, Egor                  SHKA      BIM       TL1         Shkaev Egor  Egor.Shkaev@atp-tlp.ru
# •	Ignatiev, Nikita                INI          OV       PRAK       Ignatiev Nikita  Nikita.Ignatiev@atp-tlp.ru 
# •	Dolinskiy, Alexander     ADL        OV       PRAK       Dolinskiy Alexander Alexander.Dolinskiy@atp-tlp.ru
# •	Perkhalyuk, Fedor         PDE        VK          Perkhalyuk Fedor Fedor.Perkhalyuk@atp-tlp.ru
# •	Volodina Anastasia        VAN      VK          Volodina Anastasia  Anastasia.Volodina@atp-tlp.ru
