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


class_1 = ClassName(class_name='20 Minute HIIT Training',
                    description='This class will burn 12-16 calories per minute \
                    through different intervals of speeds over the 20 min class.',
                    user_id=1, category_id=1)
session.add(class_1)
session.commit()

class_2 = ClassName(class_name='5k Fun Run',
                    description='This class will burn \
                    8-12 calories per minute through steady state heart \
                    rate zone running for 30 minutes of fun.',
                    user_id=1, category_id=1)
session.add(class_2)
session.commit()

class_3 = ClassName(class_name='Marathon Prep',
                    description='This class will burn 8-12 calories per minute \
                    getting you ready for that half or ful marathon.',
                    user_id=1, category_id=1)
session.add(class_3)
session.commit()

# Walking category and its classes
Category2 = Category(category_name='Walking', user_id=1)
session.add(Category2)
session.commit()


class_1 = ClassName(class_name='Mountain Walk',
                    description='This class will take you on a journey of inclines \
                    as well as different intervals of speeds over the 30 min class.',
                    user_id=1, category_id=2)
session.add(class_1)
session.commit()

class_2 = ClassName(class_name='Beach Stroll',
                    description='This class is designed as a nice cool down walk  \
                    increasing the blood flow through the lower body \
                                 followed by static stretching.',
                    user_id=1, category_id=2)
session.add(class_2)
session.commit()

class_3 = ClassName(class_name='Power Walk 1.0',
                    description='This class is designed to get your legs moving \
                    at a fast pace to increase the heart rate between 55-65% \
                     of your heart rate max.',
                    user_id=1, category_id=2)
session.add(class_3)
session.commit()


# Boxing category and its classes
Category3 = Category(category_name='Boxing', user_id=1)
session.add(Category3)
session.commit()

class_1 = ClassName(class_name='Boxing Conditioning',
                    description="Boxing Conditioning teaches basic boxing skills\
                                 and techniques, designed to increase muscular \
                                strength and cardio endurance—the perfect class\
                                 to get shredded! Boxing Conditioning will include \
                                cardio calisthenics, shadow boxing, bag work (150lb. bag)\
                                 and core strengthening exercises. You will sweat like\
                                 crazy, build a rock solid core and burn hundreds of calories.",
                    user_id=1, category_id=3)
session.add(class_1)
session.commit()

class_2 = ClassName(class_name='Fight Heavy',
                    description="Train like a champion with Fight FIT, our one-of-a-kind \
                     class where you'll learn basic MMA skills with a cardio kick. Fight \
                      FIT simulates a real UFC Championship fight with five five-minute rounds,\
                       utilizing various equipment such as grappling dummies and hanging bags.\
                        A basic class includes cardio calisthenics: punch, kick, knee, and elbow\
                         strikes; sprawls; grounded bags; pummeling the bags; break fall; bag\
                          work, and core strengthening exercises.",
                    user_id=1, category_id=3)
session.add(class_2)
session.commit()

class_3 = ClassName(class_name='Youth Boxing',
                    description="mixed-level class focuses on developing students' boxing skills\
                     and physical fitness. Donté's original and educational approach to teaching \
                     is what makes this class popular with kids and loved by families",
                    user_id=1, category_id=3)
session.add(class_3)
session.commit()

# Dance category and its classes
Category4 = Category(category_name='Dance', user_id=1)
session.add(Category4)
session.commit()


class_1 = ClassName(class_name='Zumba',
                    description="If you enjoy moving and shaking your hips to a Latin beat,\
                     you'll love this dance workout. No partners are needed and regular\
                      tennis shoes are recommended. Salsa, Reggaeton and more. This is\
                       more of a party than a workout! Don’t miss it! Suitable for all levels. \
    Train like a true dancer and enjoy the cardiovascular and body-shaping benefits of a \
    dynamic workout that tones muscles, develops core strength and increases balance.\
     A full dance fitness workout! Dance classes are led by energetic and highly \
     qualified fitness instructors.",
                    user_id=1, category_id=4)
session.add(class_1)
session.commit()

class_2 = ClassName(class_name='Salsa Hop',
                    description="Burn up the dance floor\
                     and burn calories Salsa Hop blends hip \
    hop and dance moves, making them simple and easy to follow!\
    Anyone can do this! This workout feels more like a night on the town\
    than exercise. Drop the pounds \
    and get rapid results while you dance, dance, dance!",
                    user_id=1, category_id=4)
session.add(class_2)
session.commit()

class_3 = ClassName(class_name='Cardio Funk Dance Party',
                    description="Utilizing pumpin' music from the 80's, 90's and\
                     today's hits, Cardio Funk will get you sweatin' and groovin\
                     ' while dancing to basic dance steps and burning calories. \
                     The instructor will break down each move, step-by-step, so \
                    the class will easily learn the entire routine by the finish",
                    user_id=1, category_id=4)
session.add(class_3)
session.commit()

print('Items have been added successfully')


