from pydantic import BaseSettings


class Config(BaseSettings):
    # SQLALCHEMY_DATABASE_URI = "sqlite:///sqlite.db"
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://postgres:postgres@localhost/crystalcv"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

config = Config()
