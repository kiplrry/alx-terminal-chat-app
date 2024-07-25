from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.exc import IntegrityError, OperationalError
from dotenv import dotenv_values

config = dotenv_values('.env')


class Storage():
    """The Storage Class"""

    __engine = None
    __session = None

    def __init__(self, base) -> None:
        """initializing the class"""
        USER = config['USER']
        PASS = config['PASS']
        HOST = config['HOST']
        DB = config['DB']
        self.base = base
        try:
            self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                          format(USER, PASS, HOST, DB))
        except OperationalError as err:
            print(f'err occured {err}')

    def save(self, obj) -> int:
        """Saves the obj to storage"""
        self.__session.commit()
        return obj.id

    def new(self, obj):
        """Saves obj to session"""
        self.__session.add(obj)

    def all(self, cls, offset: int = 0, limit: int = 100):
        """query on the current database session"""
        vals = self.__session.query(cls).offset(offset).limit(limit).all()
        return vals

    def reload(self):
        """reloads the session"""
        # self.base.metadata.drop_all(bind=self.__engine)
        self.base.metadata.create_all(bind=self.__engine)
        print('reloaded')
        print(self.base.metadata.tables.keys())
        sess = sessionmaker(bind=self.__engine, expire_on_commit=False)
        scoped = scoped_session(sess)
        self.__session = scoped

    def delete(self, obj):
        """deletes the obj in storage"""
        if obj:
            self.__session.delete(obj)
            self.__session.commit()

    def get(self, cls, id):
        """gets an object"""
        if cls and id:
            obj = self.__session.query(cls).filter_by(id=id).first()
            return obj
        return None

    def close(self):
        """close the session"""
        self.__session.remove()

    def count(self, cls):
        """Count obj in DB"""
        count = self.__session.query(cls).count()
        return count

    def query(self, cls):
        """Return query"""
        return self.__session.query(cls)
    
    def filter_by(self, cls, **kwargs):
        
        return self.__session.query(cls).filter_by(**kwargs).all()
    