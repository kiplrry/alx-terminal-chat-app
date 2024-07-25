from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, DateTime, String, Table, ForeignKey
from datetime import datetime, time
from dataclasses import dataclass
from app.database import Storage


Base  = declarative_base()
storage = Storage(Base)

@dataclass
class BaseModel:
    """basemodel"""

    id = Column(Integer(), primary_key=True, autoincrement=True)
    created_at = Column(DateTime(), default=datetime.utcnow())
    updated_at = Column(DateTime(), default=datetime.utcnow())


    def __init__(self, **kwargs) -> None:
        """initialize the instance"""
        nots = ['created_at', 'updated_at', 'id']
        if kwargs:
            for k, v in kwargs.items():
                if k in nots:
                    continue
                setattr(self, k, v)
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
    def __repr__(self) -> str:
        return f"[{self.__class__.__name__}] ({self.id})"

    def to_dict(self, save_fs=None):
        """returns a dictionary containing all keys/values of the instance"""
        new_dict = self.__dict__.copy()
        if "created_at" in new_dict:
            new_dict["created_at"] = new_dict["created_at"].strftime(time)
        if "updated_at" in new_dict:
            new_dict["updated_at"] = new_dict["updated_at"].strftime(time)
        new_dict["__class__"] = self.__class__.__name__
        if "_sa_instance_state" in new_dict:
            del new_dict["_sa_instance_state"]
        if save_fs is None:
            if "password" in new_dict:
                del new_dict["password"]
        return new_dict

    def save(self) -> int:
        """saves the obj"""
        self.updated_at = datetime.utcnow()
        storage.new(self)
        id = storage.save(self)
        return id

    @classmethod
    def delete(cls, obj):
        """deletes the obj instance"""
        storage.delete(obj)

    def update(self, **kwargs):
        """updates the obj instance"""
        if kwargs:
            kwargs.pop('id', None)
            kwargs.pop('updated_at', None)
            kwargs.pop('created_at', None)

            for arg, val in kwargs.items():
                setattr(self, arg, val)
        self.save()
        return self

    @classmethod
    def get(cls, id: int):
        """gets an instance using its id"""
        obj = storage.get(cls=cls, id=id)
        return obj

    @classmethod
    def all(cls):
        """return all instances of a cls"""
        all_obj = storage.all(cls)
        return all_obj
    
    @classmethod
    def filter(cls, **kwargs):
        """filter a cls"""
        filt = storage.filter_by(cls, **kwargs)
        return filt
    
    @classmethod
    def query(cls):
        '''returns a session query'''
        return storage.query(cls)


user_room_association = Table(
    'user_room', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('room_id', Integer, ForeignKey('rooms.id'))
)

class User(BaseModel, Base):
    """class user"""
    __tablename__ = 'users'

    username = Column(String(25), default='none', unique=True, index=True)
    password = Column(String(60))
    sid = Column(String(60))
    sent_mess = relationship('Message', backref='from_user', foreign_keys='Message.from_id')
    recv_mess = relationship('Message', backref='to_user', foreign_keys='Message.to_id')
    rooms = relationship('Room', secondary=user_room_association, back_populates='users')

class Room(BaseModel, Base):
    """Room class"""
    __tablename__ = 'rooms'

    name = Column(String(60), nullable=False, unique=True)
    messages = relationship('Message', backref='room')
    users = relationship('User', secondary=user_room_association ,back_populates='rooms')

class Message(BaseModel, Base):
    __tablename__ = 'messages'

    from_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    to_id = Column(Integer, ForeignKey('users.id'))
    room_id = Column(Integer, ForeignKey('rooms.id'))
    content = Column(String(255), nullable=False)

    def __str__(self) -> str:
        return self.to_dict()