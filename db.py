import enum
import datetime
import random as rn
import string
import hashlib

# http://docs.sqlalchemy.org/en/latest/orm/tutorial.html
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///:memory:', echo=True)

Base = declarative_base()
class User(Base):
  __tablename__ = 'users'

  id = Column(Integer, primary_key=True)
  name = Column(String, nullable=False)
  password = Column(String, nullable=False)
  salt = Column(String, nullable=False)

  def __repr__(self):
    return "User %d %s" % (self.id, self.name)

class Gender(enum.Enum):
  male = 1
  female = 2
  other = 0

class Level(enum.Enum):
  low = 0
  mid = 1
  high = 2

class FitnessStatus(Base):
  __tablename__ = 'fitness_data'

  id = Column(Integer, primary_key=True)
  age = Column(Integer, nullable=False)
  user_id = Column(Integer, ForeignKey('users.id'))
  time_created = Column(DateTime, default=datetime.datetime.utcnow)
  time_updated = Column(DateTime, default=datetime.datetime.utcnow)
  gender = Column(Enum(Gender), nullable=False)
  current_fitness_level = Column(Enum(Level), default = Level.mid)
  weight = Column(Float, nullable=False) # Pounds
  height = Column(Float, nullable=False) # Meters



Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

session = Session()

def create_user(username, encrypted_pass):
  if session.query(User).filter_by(name=username).first() != None:
    return 409
  salt = ''.join([rn.choice(string.ascii_letters + string.digits) for n in xrange(32)])
  saved = hashlib.sha256(salt + encrypted_pass).hexdigest()
  new_user = User(name = username, password = saved, salt = salt)
  session.add(new_user)
  session.commit()
  return 201

def login_user(username, encrypted_pass):
  user = session.query(User).filter_by(name=username).first()
  if user == None: return 400
  hashed = hashlib.sh256(user.salt + encrypted_pass).hexdigest()
  if hashed != user.password: return 401
  return 200

def add_fitness(fitness, user_id):
  new_fitness = Fitness(
    age=fitness['age'],
    gender=fitness['gender'],
    user_id=user_id,
    current_fitness_level=fitness['fitness_level'],
    height=fitness['height'],
    weight=fitness['weight'])
  session.add(new_fitness)
  session.commit()
  return 201

