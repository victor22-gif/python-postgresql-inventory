import psycopg
import getpass


def get_connection():
    password = getpass.getpass("PostgreSQL password: ")

    return psycopg.connect(
        dbname="store",
        user="emmanuel",
        host="127.0.0.1",
        port=5432,
        password=password,
    )


def create_product():
    name = input("Product name: ").strip()

    if not name:
        print("Product name cannot be empty.")
        return

    try:
        price = input("Price: ").strip()
        quantity = input("Quantity: ").strip()

        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO products (name, price, quantity)
                    VALUES (%s, %s, %s)
                    RETURNING id, name, price, quantity;
                    """,
                    (name, price, quantity),
                )

                product = cursor.fetchone()

        print(f"Product created: {product}")

    except (psycopg.Error, ValueError) as error:
        print(f"Could not create product: {error}")


def get_products():
    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT id, name, price, quantity, created_at
                    FROM products
                    ORDER BY id;
                    """
                )

                products = cursor.fetchall()

        if not products:
            print("\nNo products found.")
            return

        print("\n" + "=" * 100)
        print("PRODUCT INVENTORY".center(100))
        print("=" * 100)


        print(
            f"{'ID':<5}"
            f"{'PRODUCT NAME':<30}"
            f"{'PRICE (NGN)':>12}"
            f"{'QUANTITY':>10}"
            f"{'DATE CREATED':>28}"
        )

        print("-" * 100)

        for product in products:
            product_id, name, price, quantity, created_at = product

            print(
                f"{product_id:<15}"
                f"{name:<30}"
                f"{price:>15,.2f}"
                f"{quantity:>12,}"
                f"{created_at.strftime('%Y-%m-%d %H:%M'):>28}"
            )

        print("=" * 100)
        print(f"Total products: {len(products)}")

    except psycopg.Error as error:
        print(f"Could not retrieve products: {error}")



def get_product():
    try:
        product_id = int(input("Product ID: "))

        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT id, name, price, quantity, created_at
                    FROM products
                    WHERE id = %s;
                    """,
                    (product_id,),
                )

                product = cursor.fetchone()

        if product is None:
            print("Product not found.")
        else:
            print(product)

    except ValueError:
        print("Product ID must be an integer.")
    except psycopg.Error as error:
        print(f"Could not retrieve product: {error}")


def update_product():
    try:
        product_id = int(input("Product ID: "))
    except ValueError:
        print("Product ID must be an integer.")
        return

    name = input("New product name: ").strip()
    price = input("New price: ").strip()
    quantity = input("New quantity: ").strip()

    if not name:
        print("Product name cannot be empty.")
        return

    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE products
                    SET name = %s,
                        price = %s,
                        quantity = %s
                    WHERE id = %s
                    RETURNING id, name, price, quantity;
                    """,
                    (name, price, quantity, product_id),
                )

                product = cursor.fetchone()

        if product is None:
            print("Product not found.")
        else:
            print(f"Product updated: {product}")

    except (psycopg.Error, ValueError) as error:
        print(f"Could not update product: {error}")


def delete_product():
    try:
        product_id = int(input("Product ID: "))

        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    DELETE FROM products
                    WHERE id = %s
                    RETURNING id, name;
                    """,
                    (product_id,),
                )

                product = cursor.fetchone()

        if product is None:
            print("Product not found.")
        else:
            print(f"Product deleted: {product}")

    except ValueError:
        print("Product ID must be an integer.")
    except psycopg.Error as error:
        print(f"Could not delete product: {error}")


def main():
    while True:
        print("\n===== PRODUCT MANAGEMENT =====")
        print("1. Create product")
        print("2. List products")
        print("3. Get product by ID")
        print("4. Update product")
        print("5. Delete product")
        print("0. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            create_product()
        elif choice == "2":
            get_products()
        elif choice == "3":
            get_product()
        elif choice == "4":
            update_product()
        elif choice == "5":
            delete_product()
        elif choice == "0":
            break
        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()

