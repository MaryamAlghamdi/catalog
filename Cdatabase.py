from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import LearningCourses, Base, cListItem, User

engine = create_engine('sqlite:///LcourseslcListwithusers.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance


Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()


session = DBSession()


# Create dummy user


User1 = User(name="Robo Barista", email="tinnyTim@udacity.com",
             picture='https://pbs.twimg.com/profile_images/' +
             '2671170543/18debd694829ed78203a5a36dd364160_400x400.png')
session.add(User1)
session.commit()

# Create English Course with All Items


Lcourses1 = LearningCourses(user_id=1, name="English Course")

session.add(Lcourses1)
session.commit()

lcListItem2 = cListItem(user_id=1, name="Level 1",
                        description="Entree Level English Course",
                        price="$7.50", course="Entree", Lcourses=Lcourses1)

session.add(lcListItem2)
session.commit()


lcListItem1 = cListItem(user_id=1, name="Level 9",
                        description="Advance Level English Course",
                        price="$2.99", course="Advance", Lcourses=Lcourses1)

session.add(lcListItem1)
session.commit()

lcListItem2 = cListItem(user_id=1, name="Level 2",
                        description="Entree Level English Course",
                        price="$5.50", course="Entree", Lcourses=Lcourses1)

session.add(lcListItem2)
session.commit()

lcListItem3 = cListItem(user_id=1, name="Level 6",
                        description="Easy Level English Course",
                        price="$3.99", course="Easy", Lcourses=Lcourses1)

session.add(lcListItem3)
session.commit()

lcListItem4 = cListItem(user_id=1, name="Level 3",
                        description="Entree Level English Course",
                        price="$7.99", course="Entree", Lcourses=Lcourses1)

session.add(lcListItem4)
session.commit()

lcListItem5 = cListItem(user_id=1, name="Level 7",
                        description="Intermediate Level English Course",
                        price="$1.99", course="Intermediate",
                        Lcourses=Lcourses1)

session.add(lcListItem5)
session.commit()

lcListItem6 = cListItem(user_id=1, name="Level 8",
                        description="Intermediate Level English Course",
                        price="$.99", course="Intermediate",
                        Lcourses=Lcourses1)

session.add(lcListItem6)
session.commit()

lcListItem7 = cListItem(user_id=1, name="Level 4",
                        description="Entree Level English Course",
                        price="$3.49",
                        course="Entree", Lcourses=Lcourses1)

session.add(lcListItem7)
session.commit()

lcListItem8 = cListItem(user_id=1, name="Level 5",
                        description="Entree Level English Course",
                        price="$5.99", course="Entree", Lcourses=Lcourses1)

session.add(lcListItem8)
session.commit()


# Create French Course with All Items


Lcourses1 = LearningCourses(user_id=1, name="French Course ")

session.add(Lcourses1)
session.commit()

lcListItem9 = cListItem(user_id=1, name="Level 1",
                        description="Entree Level French Course",
                        price="$8.99", course="Entree", Lcourses=Lcourses1)

session.add(lcListItem9)
session.commit()


lcListItem1 = cListItem(user_id=1, name="Level 5",
                        description="Easy Level French Course",
                        price="$2.99", course="Eeasy Level French Course",
                        Lcourses=Lcourses1)

session.add(lcListItem1)
session.commit()

lcListItem2 = cListItem(user_id=1, name="Level 2",
                        description="Entree Level French Course",
                        price="$10.95", course="Entree", Lcourses=Lcourses1)

session.add(lcListItem2)
session.commit()

lcListItem3 = cListItem(user_id=1, name="Level 8",
                        description="Advance Level French Course",
                        price="$7.50",
                        course="Advance", Lcourses=Lcourses1)

session.add(lcListItem3)
session.commit()

lcListItem4 = cListItem(user_id=1, name="Level 3",
                        description="Entree Level French Course",
                        price="$8.95", course="Entree", Lcourses=Lcourses1)

session.add(lcListItem4)
session.commit()

lcListItem2 = cListItem(user_id=1, name="Level 4",
                        description="Entree Level French Course",
                        price="$9.50", course="Entree", Lcourses=Lcourses1)

session.add(lcListItem2)
session.commit()

lcListItem10 = cListItem(user_id=1, name="Level 6",
                         description="Easy Level French Course",
                         price="$1.99", course="Easy", Lcourses=Lcourses1)

session.add(lcListItem10)
session.commit()

lcListItem11 = cListItem(user_id=1, name="Level 7",
                         description="Intermediate Level French Course",
                         price="$1.99", course="Intermediate",
                         Lcourses=Lcourses1)

session.add(lcListItem11)
session.commit()

print "added items!"
