"""
This module defines the routes for rental contract operations in the RentalService API.

Routes:
    - POST /api/v1/rentals: Create a new rental contract.
    - GET /api/v1/rentals/all: Retrieve all rental contracts.
    - GET /api/v1/rentals/<int:rental_id>: Retrieve a single rental contract by its ID.
    - PUT /api/v1/rentals/<int:rental_id>: Update an existing rental contract by its ID.
    - DELETE /api/v1/rentals/<int:rental_id>: Delete a rental contract by its ID.

Each route interacts with the rental repository to perform CRUD operations on rental contracts.

Functions:
    - create_rental_contract(): Handles the creation of a new rental contract.
    - get_all_rental_contracts(): Retrieves all rental contracts.
    - get_rental_contract(rental_id): Retrieves a rental contract by its ID.
    - update_rental_contract(rental_id): Updates a rental contract by its ID.
    - delete_rental_contract(rental_id): Deletes a rental contract by its ID.

Dependencies:
    - Flask: Used for creating the API routes and handling HTTP requests and responses.
    - rental_repository: Contains the database operations for rental contracts.
"""

from flask import Blueprint, jsonify, request
from repositories.rental_repository import (
    db_create_rental_contract, db_get_all_rental_contracts, db_get_rental_contract_by_id, db_update_rental_contract, db_delete_rental_contract
)

rental_routes = Blueprint('rental_routes', __name__)

# Create a new rental contract (/api/v1/rentals)
@rental_routes.route('', methods=['POST'])
def create_rental_contract():
    data = request.json
    required_fields = ['start_date', 'end_date', 'start_km', 'contracted_km', 'monthly_price', 'car_id', 'customer_id']

    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        rental_id = db_create_rental_contract(data)
        return jsonify({"message": "Rental contract created", "rental_id": rental_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Get all rental contracts
@rental_routes.route('/all', methods=['GET'])
def get_all_rental_contracts():
    try:
        rentals = db_get_all_rental_contracts()
        return jsonify(rentals), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Get a single rental contract by ID
@rental_routes.route('/<int:rental_id>', methods=['GET'])
def get_rental_contract(rental_id):
    try:
        rental = db_get_rental_contract_by_id(rental_id)
        return jsonify(rental), 200 if rental else 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Update a rental contract
@rental_routes.route('/<int:rental_id>', methods=['PUT'])
def update_rental_contract(rental_id):
    data = request.json
    try:
        updated_rows = db_update_rental_contract(rental_id, data)
        if updated_rows == 0:
            return jsonify({"error": "Rental contract not found"}), 404
        return jsonify({"message": "Rental contract updated"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Delete a rental contract
@rental_routes.route('/<int:rental_id>', methods=['DELETE'])
def delete_rental_contract(rental_id):
    try:
        deleted_rows = db_delete_rental_contract(rental_id)
        if deleted_rows == 0:
            return jsonify({"error": "Rental contract not found"}), 404
        return jsonify({"message": "Rental contract deleted"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500