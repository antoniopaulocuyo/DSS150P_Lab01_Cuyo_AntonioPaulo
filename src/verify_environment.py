from sqlalchemy import create_engine, text

DATABASE_URL = "postgresql+psycopg2://dss150p:dss150p_lab@localhost:5432/dss150p_lab"
engine = create_engine(DATABASE_URL)

with engine.connect() as connection:
    print(connection.execute(text("SELECT version();")).scalar())
    print(connection.execute(text("SELECT current_database();")).scalar())