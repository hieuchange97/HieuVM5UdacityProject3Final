import os
from urllib.parse import quote

app_dir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig:
    DEBUG = True
    POSTGRES_URL=""  #TODO: Update value
    POSTGRES_USER="" #TODO: Update value
    POSTGRES_PW=""  #TODO: Update value
    POSTGRES_DB=""   #TODO: Update value
    DB_URL = 'postgresql://{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER,pw=POSTGRES_PW,url=POSTGRES_URL,db=POSTGRES_DB)
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI') or DB_URL
    CONFERENCE_ID = 1
    SECRET_KEY = os.getenv('SECRET_KEY')
    SERVICE_BUS_CONNECTION_STRING = os.getenv('SERVICE_BUS_CONNECTION_STRING')
    ADMIN_EMAIL_ADDRESS = "minhhieuvu9497@gmail.com"
    SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')

class DevelopmentConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    DEBUG = False