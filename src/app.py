"""This is my lab to experiment with Docker, Flask and Python - based on
course 'Pluralsight - Developing Python 3 Apps with Docker'
by Steven Haines all credits belongs to author
"""
import logging.config
from flask import Flask, jsonify, request
from sqlalchemy import exc
import configparser
import debugpy
import os
from db import db
from Product import Product

# configure the logging package from the logging ini file
logging.config.fileConfig("/config/logging.ini", disable_existing_loggers=False)

#Get a logger from our module
log = logging.getLogger(__name__)

# Setup debugger
debug = os.getenv('DEBUG', 'False')
if debug == 'True':
    debugpy.listen(("0.0.0.0", 5678))
    log.info('Started debugger on port 5678')
def get_database_url():
    # Load our database configuration
    config = configparser.ConfigParser()
    config.read('/config/db.ini')
    database_configuration = config['mysql']
    host = database_configuration['host']
    username = database_configuration['username']
    db_password = open('/run/secrets/db_password')
    password = db_password.read()
    database = database_configuration['database']
    database_url = f'mysql://{username}:{password}@{host}/{database}'
    log.info(f'Connecting to database: {database_url}')
    return database_url


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = get_database_url()
db.init_app(app)

# curl -v http://localhost/products
@app.route("/products")
def get_products():
    """This function create an endpoint to show all products on json format"""
    log.debug('GET /products')
    try:
        products = [product.json for product in Product.find_all()]
        return jsonify(products)
    except exc.SQLAlchemyError:
        log.exception('An exception occurred while retrieving all products')
        return 'An exception occurred while retrieving all products', 500


# curl -v http://localhost/product/1
@app.route("/product/<int:prod_id>")
def get_product(prod_id):
    """This function create an endpoint to show a product based on prod_id"""
    log.debug('GET /product/{prod_id}')

    try:
        product = Product.find_by_prod_id(prod_id)
        if product:
            return jsonify(product.json)
        log.warning(f'Product with prod_id {prod_id} not found')
        return f"Product with prod_id {prod_id} not found", 404
    except exc.SQLAlchemyError:
        log.exception(f'An exception occurred while retrieving product {prod_id}')
        return f'An exception occurred while retrieving product {prod_id}', 500

# curl --header "Content-Type: application/json" --request POST --data '{"name" : "product3"}' -v http://localhost/product
@app.route('/product', methods=['POST'])
def post_product():
    """Create a new product on database"""
    # Retrieve the product from the request body
    request_product = request.json
    log.debug(f'POST /product with product:{request_product}')

    # Create a new product
    product = Product(None, request_product['name'])

    try:
        # Save the product to the Database
        product.save_to_db()

        # Return the new product back to the client
        return jsonify(product.json), 201
  
    except exc.SQLAlchemyError:
        log.exception(f'An exception occurred while creating product with name {product.name}')
        return f'An exception occurred while creating product with name {product.name}', 500

# curl --header "content-Type: application/json" --request PUT --data '{"name" : "Update product2"}' -v http://localhost/product/2
@app.route('/product/<int:prod_id>', methods=['PUT'])
def put_product(prod_id):
    """Update a product name based on prod_id"""
    log.debug(f'PUT /product/{prod_id}')

    try:
        existing_product = Product.find_by_prod_id(prod_id)

        if existing_product:
            # Get the request payload
            update_product = request.json

            existing_product.name = update_product['name']
            existing_product.save_to_db()

            return jsonify(existing_product.json), 200
        
        log.warning(f'PUT /product/{prod_id}: Existing product not found')
        return f'Product with prod_id {prod_id} not found', 404
    
    except exc.SQLAlchemyError:
        log.exception(f'An exception occurred while updating product with name: {update_product.name}')
        return f'An exception occurred while updating product with name: {update_product.name}', 500

        
# curl --request DELETE -v http://localhost/product/2
@app.route('/product/<int:prod_id>', methods=['DELETE'])
def delete_product(prod_id):
    """Delete a product based on prod_id"""
    log.debug(f'DELETE /product/{prod_id}')
    try:
        existing_product = Product.find_by_prod_id(prod_id)
        if existing_product:
            existing_product.delete_from_db()
            return jsonify({
            'message': f'Deleted product with prod_id {prod_id}'
                }), 200
        
        log.warning(f'DELETE /product/{prod_id}: Existing product not found')
        return f'Product with prod_id {prod_id} not found', 404
    
    except exc.SQLAlchemyError:
        log.exception(f'An exception occurred while deleting the product with prod_id: {prod_id}')
        return f'An exception occurred while deleting the product with prod_id: {prod_id}', 500


#main()
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
