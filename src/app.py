"""This is my lab to experiment with Docker, Flask and Python - based on
course 'Pluralsight - Developing Python 3 Apps with Docker'
by Steven Haines all credits belongs to author
"""
from flask import Flask, jsonify, request
from db import db
from Product import Product


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:password@db/products'
db.init_app(app)

# curl -v http://localhost/products
@app.route("/products")
def get_products():
    """This function create an endpoint to show all products on json format"""
    products = [product.json for product in Product.find_all()]
    return jsonify(products)

# curl -v http://localhost/product/1
@app.route("/product/<int:prod_id>")
def get_product(prod_id):
    """This function create an endpoint to show a product based on prod_id"""
    product = Product.find_by_prod_id(prod_id)
    if product:
        return jsonify(product.json)
    return f"Product with prod_id {prod_id} not found", 404

# curl --header "Content-Type: application/json" --request POST --data '{"name" : "product3"}' -v http://localhost/product
@app.route('/product', methods=['POST'])
def post_product():
    """Create a new product on database"""
    # Retrieve the product from the request body
    request_product = request.json

    # Create a new product
    product = Product(None, request_product['name'])

    # Save the product to the Database
    product.save_to_db()

    # Return the new product back to the client
    return jsonify(product.json), 201

# curl --header "content-Type: application/json" --request PUT --data '{"name" : "Update product2"}' -v http://localhost/product/2
@app.route('/product/<int:prod_id>', methods=['PUT'])
def put_product(prod_id):
    """Update a product name based on prod_id"""

    existing_product = Product.find_by_prod_id(prod_id)

    if existing_product:
        # Get the request payload
        update_product = request.json

        existing_product.name = update_product['name']
        existing_product.save_to_db()

        return jsonify(existing_product.json), 200
    return f'Product with prod_id {prod_id} not found', 404

# curl --request DELETE -v http://localhost/product/2
@app.route('/product/<int:prod_id>', methods=['DELETE'])
def delete_product(prod_id):
    """Delete a product based on prod_id"""
    existing_product = Product.find_by_prod_id(prod_id)

    if existing_product:
        existing_product.delete_from_db()
        return jsonify({
            'message': f'Deleted product with prod_id {prod_id}'
        }), 200
        

    return f'Product with prod_id {prod_id} not found', 404


#main()
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
