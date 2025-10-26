import os

class DevelopmentConfig:
  
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")

    USER = os.getenv("DB_USER", "root")
    PASSWORD = os.getenv("DB_PASSWORD", "")
    HOST = os.getenv("DB_HOST", "127.0.0.1")
    PORT = os.getenv("DB_PORT", "3306")
    DB = os.getenv("DB_NAME", "mechanicShopDB")

    if not SQLALCHEMY_DATABASE_URI:
        SQLALCHEMY_DATABASE_URI = (
            f"mysql+mysqlconnector://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}"
        )

    DEBUG = True


class TestingConfig:
    pass


class ProductionConfig:
    pass