"""This is my lab to experiment with Docker, Flask and Python - based on
course 'Pluralsight - Developing Python 3 Apps with Docker'
by Steven Haines all credits belongs to author
"""
from flask import Flask, jsonify, request

products = [
    {"id" : 1 , "name" : "product1"},
    {"id" : 2 , "name" : "product2"}
]

app = Flask(__name__)

# curl -v http://localhost:5000/products
@app.route("/products")
def get_products():
    """This function create an endpoint to show all products on json format"""
    return jsonify(products)

# curl -v http://localhost:5000/product/1
@app.route("/product/<int:id>")
def get_product(id):
    """This function create an endpoint to show a product based on id"""
    product_list = [product for product in products if product['id'] == id]
    if len(product_list) == 0:
        return f"Product with id {id} not found", 404
    return jsonify(product_list[0])

# curl --header "Content-Type: application/json" --request POST --data '{"name" : "product3"}' -v http://localhost:5000/product
@app.route('/product', methods=['POST'])
def post_product():
    """Create a new product on database"""
    # Retrieve the product from the request body
    request_product = request.json

    # Generenate an ID for the post
    new_id = max([product['id'] for product in products]) + 1

    # Create a new product
    new_product = {
        'id' : new_id,
        'name' : request_product['name']
    }

    # Append the new product to our product list
    products.append(new_product)

    # Return the new product back to the client
    return jsonify(new_product), 201

# curl --header "content-Type: application/json" --request PUT --data '{"name" : "Update product2"}' -v http://localhost:5000/product/2
@app.route('/product/<int:id>', methods=['PUT'])
def put_product(id):
    """Update a product name based on id"""
    # Get the request payload
    update_product = request.json

    #Find the product with the specified id
    for product in products:
        if product['id'] == id:
            # Update product name
            product['name'] = update_product['name']
            return jsonify(product), 200

    return f'Product with id {id} not found', 404


#main()
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
