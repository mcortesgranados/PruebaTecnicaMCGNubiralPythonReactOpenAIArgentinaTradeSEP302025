import os

# Example for MySQL, adjust as needed for your actual DB
SQLALCHEMY_DATABASE_URL = os.getenv(
    "SQLALCHEMY_DATABASE_URL",
    "mysql+pymysql://root:root@localhost/prueba_tecnica_nubiral"
)