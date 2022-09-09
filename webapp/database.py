from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# engine = create_engine('mysql://root:root@dbcontainer/website?charset=utf8mb4')
engine = create_engine('sqlite:///test3.db', future=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import webapp.models
    print("I did something")
    Base.metadata.create_all(bind=engine)