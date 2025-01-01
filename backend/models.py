from sqlalchemy import Column, Integer, String, Text, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()

# Email model
class Email(Base):
    __tablename__ = 'emails'

    id = Column(Integer, primary_key=True, autoincrement=True)
    message_id = Column(String, unique=True, nullable=False)  # Unique identifier for each email
    subject = Column(String)
    body = Column(Text)
    body_md = Column(Text)  # Store markdown version of the email body
    template_json = Column(Text)  # Store json template for supplier information
    template_table = Column(Text)  # Store table template

# SQLite engine setup
engine = create_engine('sqlite:///emails.db')
SessionLocal = sessionmaker(bind=engine)

# Create the table if it doesn't exist
Base.metadata.create_all(engine)
