import psycopg2
from faker import Faker
import random

# database connection parameters
# db_params = {
#     "host": "postgres://postgres:postgres@postgres-python:5433/anythink-market",
#     "database": "anythink-market",
#     "user": "postgres",
#     "password": "postgres",
# }

# connection to db
conn = psycopg2.connect(database="anythink-market", user="postgres", password="postgres", host="0.0.0.0", port="5432")
cursor = conn.cursor()

# create user table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        username VARCHAR(255),
        email VARCHAR(255),
        bio VARCHAR(255),
        image VARCHAR(255)
    )
''')
# postgres://YourUserName:YourPassword@YourHostname:5432/YourDatabaseName

# create products table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS items(
        id SERIAL PRIMARY KEY,
        slug VARCHAR(255),
        title VARCHAR(255),
        description TEXT,
        tags TEXT[],
        seller INTEGER REFERENCES users(id),
        favorited BOOLEAN,
        favorites_count INTEGER,
        image TEXT,
        body TEXT
    )
''')

# create comments table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS comments(
        id SERIAL PRIMARY KEY,
        body TEXT,
        seller INTEGER REFERENCES users(id)
    )
''')

# Generate and insert 100 users into the 'users' table
fake = Faker()
for _ in range(100):
    id = fake.unique.random_int(111111,999999)
    username = fake.user_name()
    email = fake.email()
    bio = fake.paragraph(nb_sentences=3)
    image = fake.file_path(depth=3)
    cursor.execute("INSERT INTO users VALUES (%s, %s, %s, %s, %s)", (id, username, email, bio, image))

# Generate and insert 100 products into the 'items' table
for _ in range(100):
    id = fake.unique.random_int(111111,999999)
    slug = fake.word()
    title = fake.email()
    description = fake.paragraph(nb_sentences=4)
    tags = fake.words(nb=3)
    seller = fake.user_name()
    favourited = random.choice([True, False])
    favorites_count = round(random.uniform(10, 1000), 2)
    image = fake.file_path(depth=3)
    body = fake.paragraph(nb_sentences=6)
    cursor.execute("INSERT INTO items VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (id, slug, title, description, tags, seller, favourited, favorites_count, image, body))

# Generate and insert 100 comments into the 'comments' table
for _ in range(100):
    id = fake.unique.random_int(111111,999999)
    body = fake.paragraph(nb_sentences=3)
    seller = fake.user_name()
    cursor.execute("INSERT INTO comments VALUES (%s, %s, %s)", (id, body, seller))

conn.commit()
conn.close()