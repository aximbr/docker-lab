"""This is my lab to experiment with Docker, Flask and Python - based on
course 'Pluralsight - Developing Python 3 Apps with Docker'
by Steven Haines all credits belongs to author
"""
from flask import Flask, jsonify

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

#main()
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
