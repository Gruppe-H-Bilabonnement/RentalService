"""
This module provides functions to interact with the rental contracts in the database.

Functions:
- db_create_rental_contract(data): Creates a new rental contract with the provided data.
- db_get_all_rental_contracts(): Retrieves all rental contracts from the database.
- db_get_rental_by_id(rental_id): Retrieves a single rental contract by its ID.
- db_update_rental(rental_id, data): Updates an existing rental contract with the provided data.
- db_delete_rental(rental_id): Deletes a rental contract by its ID.
"""

import sqlite3
from database.connection import create_connection

# Create a new rental contract
def db_create_rental_contract(data):
    try:
        connection = create_connection()
        cursor = connection.cursor()

        query = """
            INSERT INTO rental_contracts (start_date, end_date, start_km, contracted_km, monthly_price, car_id, customer_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        cursor.execute(query, (
            data['start_date'],
            data['end_date'],
            data['start_km'],
            data['contracted_km'],
            data['monthly_price'],
            data['car_id'],
            data['customer_id']
        ))

        connection.commit()
        return True

    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False
    finally:
        connection.close()

# Retrieve all rental contracts
def db_get_all_rental_contracts():
    try:
        connection = create_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM rental_contracts")
        rentals = cursor.fetchall()
        return [dict(row) for row in rentals]

    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        connection.close()

# Retrieve a single rental contract by ID
def db_get_rental_by_id(rental_id):
    try:
        connection = create_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM rental_contracts WHERE id = ?", (rental_id,))
        rental = cursor.fetchone()
        return dict(rental) if rental else None

    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        connection.close()

# Update a rental contract
def db_update_rental(rental_id, data):
    try:
        connection = create_connection()
        cursor = connection.cursor()

        query = """
            UPDATE rental_contracts
            SET start_date = ?, end_date = ?, start_km = ?, contracted_km = ?, monthly_price = ?, car_id = ?, customer_id = ?, updated_at = datetime('now')
            WHERE id = ?
        """
        cursor.execute(query, (
            data['start_date'],
            data['end_date'],
            data['start_km'],
            data['contracted_km'],
            data['monthly_price'],
            data['car_id'],
            data['customer_id'],
            rental_id
        ))

        connection.commit()
        return cursor.rowcount > 0 # Return True if rows were updated

    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        connection.close()

# Delete a rental agreement
def db_delete_rental(rental_id):
    try:
        connection = create_connection()
        cursor = connection.cursor()

        cursor.execute("DELETE FROM rental_agreements WHERE id = ?", (rental_id,))
        connection.commit()
        return cursor.rowcount > 0 # Return True if rows were deleted

    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        connection.close()