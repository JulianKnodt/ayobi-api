import random as rn
import string
import hashlib

# http://docs.sqlalchemy.org/en/latest/orm/tutorial.html
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///:memory:', echo=True)

Base = declarative_base()
class User(Base):
  __tablename__ = 'users'

  id = Column(Integer, primary_key=True)
  name = Column(String)
  password = Column(String)
  salt = Column(String)

  def __repr__(self):
    return "User %d %s" % (self.id, self.name)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

session = Session()

def createUser(username, encrypted_pass):
  if session.query(User).filter_by(name=username).first() != None:
    return 409
  salt = ''.join([rn.choice(string.ascii_letters + string.digits) for n in xrange(32)])
  saved = hashlib.sha256(salt + encrypted_pass).hexdigest()
  new_user = User(name = username, password = saved, salt = salt)
  session.add(new_user)
  session.commit()
  return 201

def loginUser(username, encrypted_pass):
  user = session.query(User).filter_by(name=username).first()
  if user == None: return 400
  hashed = hashlib.sh256(user.salt + encrypted_pass).hexdigest()
  if hashed != user.password: return 401
  return 200

