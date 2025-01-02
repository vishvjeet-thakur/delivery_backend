from sqlmodel import SQLModel , create_engine ,Session

#This database url should be put in config file , for demo putting here
DATABASE_URL= "postgresql://postgres:1234@localhost:5432/demo"
engine = create_engine(DATABASE_URL) # to connect with the database

# to initialize db by creating all the models in db
def init_db():
    SQLModel.metadata.create_all(engine)

# new session which will be used per request and releasing resources as soon as response is sent for better resources
def get_session():
    with Session(engine) as session:
        yield session

