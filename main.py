from fastapi import FastAPI
import uvicorn
import psycopg2
import requests
# from config import user, host, password, db_name
host = 'localhost'
user = 'postgres'
password = 'Zxc1259663oliver'
db_name = 'products_data'


app = FastAPI()

@app.post('/put_in_db/{name}/{price}/{description}')
def put_in_db(name: str, price: str, description: str):
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        with connection.cursor() as cursor:
            cursor.execute(f"insert into prod_data(name, price, description) values ('{name}', '{price}', '{description}')")
            cursor.execute("select id from prod_data order by id desc limit 1")
            last_id = cursor.fetchone()
        connection.commit()
        return last_id
    except Exception as _ex:
        print('[INFO]', _ex)

    finally:
        if psycopg2.connect(
                host=host,
                user=user,
                password=password,
                database=db_name
        ):
            psycopg2.connect(
                host=host,
                user=user,
                password=password,
                database=db_name
            ).close()

@app.get('/take_from_db/{id}')
def take_from_db(id: int):
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        with connection.cursor() as cursor:
            cursor.execute(f"select name, price, description, id from prod_data where id = {id}")
            about_prod = cursor.fetchall()
        connection.commit()
        return about_prod
    except Exception as _ex:
        print('[INFO]', _ex)

    finally:
        if psycopg2.connect(
                host=host,
                user=user,
                password=password,
                database=db_name
        ):
            psycopg2.connect(
                host=host,
                user=user,
                password=password,
                database=db_name
            ).close()

@app.post('/put_address_in_db/{address}/{id}')
def put_address_in_db(address: str, prod_id: int):
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        with connection.cursor() as cursor:
            data = requests.get(f'http://127.0.0.1:8000/take_from_db/{prod_id}').json()
            name = str(data[0][0])
            print(name, prod_id, address)
            cursor.execute(f"insert into offers_data(name, address, prod_id) values ('{name}', '{address}', '{prod_id}')")
        connection.commit()
    except Exception as _ex:
        print('[INFO]', _ex)

    finally:
        if psycopg2.connect(
                host=host,
                user=user,
                password=password,
                database=db_name
        ):
            psycopg2.connect(
                host=host,
                user=user,
                password=password,
                database=db_name
            ).close()

if __name__ == '__main__':
    uvicorn.run(app)

