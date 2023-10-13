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

# create items table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS items(
        id SERIAL PRIMARY KEY,
        slug VARCHAR(255),
        title VARCHAR(255),
        description TEXT,
        body TEXT,
        image TEXT,
        seller_id INTEGER REFERENCES users(id)          
        
    )
''')

# create comments table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS comments(
        id SERIAL PRIMARY KEY,
        body TEXT,
        seller_id INTEGER REFERENCES users(id),
        item_id INTEGER REFERENCES items(id)
    )
''')


# Generate and insert 100 users into the 'users' table
fake = Faker()
start_range = 100
end_range = 201
num_unique_ids = 100  # Change this to the number of unique integers you need

unique_ids = set()  # Create a set to ensure uniqueness
while len(unique_ids) < num_unique_ids:
    unique_ids.add(fake.unique.random_int(start_range, end_range))

# Convert the set to a list
unique_ids_list = list(unique_ids)

# Generate and insert 100 users into the 'users' table
for _ in range(100):
    id = random.choice(unique_ids_list)
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
    body = fake.paragraph(nb_sentences=6)
    image = fake.file_path(depth=3)
    seller_id = fake.random_int(111111,999999)      
    
    cursor.execute("INSERT INTO items VALUES (%s, %s, %s, %s, %s, %s, %s)", (id, slug, title, description, body, image, seller_id ))

# Generate and insert 100 comments into the 'comments' table
for _ in range(100):
    id = fake.unique.random_int(111111,999999)
    body = fake.paragraph(nb_sentences=3)
    seller_id = random.choice(unique_ids_list)
    item_id = fake.random_int(111111,999999)
    cursor.execute("INSERT INTO comments VALUES (%s, %s, %s, %s)", (id, body, seller_id, item_id))

conn.commit()
conn.close()