import os

SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') #kyunki heroku pe database_url se loaded hai settings mein jaake config vars se pta chla heroku ke. and .env mein apne 
#local database ka bhi naam yehi rakha hai taki agr local chalana ho toh bhi chl jaye
SECRET_KEY = os.environ.get('SECRET_KEY')
SQLALCHEMY_TRACK_MODIFICATIONS = False