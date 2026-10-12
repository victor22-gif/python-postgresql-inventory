import getpass
import psycopg


def create_product_table():
    password = getpass.getpass("PostgreSQL password: ")


    try:
        with psycopg.connect(
                dbname="store",
                user="emmanuel",
                host="127.0.0.1",
                port=5432,
                password=password,
                ) as connection:

            with connection.cursor() as cursor:
                cursor.execute("""
                CREATE TABLE IF NOT EXISTS products (
                id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                name VARCHAR(100) NOT NULL UNIQUE,
                price NUMERIC(12, 2) NOT NULL
                CHECK (PRICE >= 0),
                quantity INTEGER NOT NULL DEFAULT 0
                CHECK (quantity >= 0),
                created_at TIMESTAMP NOT NULL
                DEFAULT CURRENT_TIMESTAMP
                );
                """)

            print("Product table created successfully.")

    except psycopg.Error as error:
        print(f"Database error: {error}")


if __name__ == "__main__":
    create_product_table()
