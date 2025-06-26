from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# Database in memory for testing purposes
engine_testing = create_engine("sqlite:///:memory:")

SessionTesting = sessionmaker(bind=engine_testing)

