import json
import sqlalchemy
import psycopg2
from sqlalchemy.orm import sessionmaker
from models import create_tables, Publisher, Shop, Book, Stock, Sale
DSN = "postgresql://postgres:180594@localhost:5432/DB_ORM"
engine = sqlalchemy.create_engine(DSN)

create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()


with open('tests_data.json', 'r') as fd:
    data = json.load(fd)

for record in data:
    model = {
        'publisher': Publisher,
        'shop': Shop,
        'book': Book,
        'stock': Stock,
        'sale': Sale,
    }[record.get('model')]
    session.add(model(id=record.get('pk'), **record.get('fields')))
session.commit()


input1 = input(f'Введите имя издательства:')
query = session.query(Shop).join(Stock).join(Book).join(Publisher).filter(Publisher.name.ilike(f"%{input1}%"))
for shop in query.all():
    print(f'Книги издательства {input1} можно купить в магазине {shop.name}, id магазина: {shop.id}')

session.close()
