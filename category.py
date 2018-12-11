from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import User, Category, ClassName, Base


engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


User1 = User(name='Jack Frost', email='jackfrost@yahoo.com')
session.add(User1)
session.commit()


# Running category and its classes
Category1 = Category(category_name='Running', user_id=1)
session.add(Category1)
session.commit()


class_1 = ClassName(class_name='20 Minute HIIT Training', description='This class will burn 12-16 calories per minute \
                    through different intervals of speeds over the 20 min class.', user_id=1, category_id=1)
session.add(class_1)
session.commit()

class_2 = ClassName(class_name='5k Fun Run', description='This class will burn 8-12 calories per minute \
                    through steady state heart rate zone running for 30 minutes of fun.', user_id=1, category_id=1)
session.add(class_2)
session.commit()

class_3 = ClassName(class_name='Marathon Prep', description='This class will burn 8-12 calories per minute \
                    getting you ready for that half or ful marathon.', user_id=1, category_id=1)
session.add(class_3)
session.commit()

# Walking category and its classes
Category2 = Category(category_name='Walking', user_id=1)
session.add(Category2)
session.commit()


class_1 = ClassName(class_name='Mountain Walk', description='This class will take you on a journey of inclines \
                    as well as different intervals of speeds over the 30 min class.', user_id=1, category_id=2)
session.add(class_1)
session.commit()

class_2 = ClassName(class_name='Beach Stroll', description='This class is designed as a nice cool down walk  \
                    increasing the blood flow through the lower body followed by static stretching.',
                    user_id=1, category_id=2)
session.add(class_2)
session.commit()

class_3 = ClassName(class_name='Power Walk 1.0', description='This class is designed to get your legs moving at a fast \
                    pace to increase the heart rate between 55-65% of your heart rate max.', user_id=1, category_id=2)
session.add(class_3)
session.commit()

print('Items have been added successfully')


