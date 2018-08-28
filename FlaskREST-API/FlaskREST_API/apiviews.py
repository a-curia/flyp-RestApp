"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, jsonify, request, Response, json
#from FlaskREST_API import app
from FlaskREST_API import settings
from FlaskREST_API import BookModel
from BookModel import *
from settings import *
import json


def validBookObject(bookObject):
    if ("name" in bookObject and "price" in bookObject and "isbn" in bookObject):
        return True
    else:
        return False


def valid_put_request_data(request_data):
    if("name" in request_data and "price" in request_data):
        return True
    else:
        return False


@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return 'Hello world'


@app.route('/books')
def get_all_books():
    """Renders the books page."""
    print(books)
    #return jsonify({'my-books':books})
    return jsonify({'my-books':Book.get_all_books()})


@app.route('/books/<int:myisbn>', methods=['GET'])
def get_book_by_isbn(myisbn):
    """Renders the specific book page."""
    #return_value = {}
    #for book in books:
    #    if book["isbn"] == myisbn:
    #        return_value = {
    #            'name': book["name"],
    #            'price':book["price"]
    #        }
    #print(myisbn)

    return_value = Book.get_book(mybooks)
    return jsonify(return_value)


@app.route('/books', methods=['POST'])
def add_book():
    request_data = request.get_json()
    if(validBookObject(request_data)):
        #new_book = {
        #    "name": request_data['name'],
        #    "price": request_data['price'],
        #    "isbn": request_data['isbn']
        #}
        #books.insert(0, new_book)
        Book.add_book(request_data['name'],request_data['price'],request_data['isbn'])

        response = Response("",201,mimetype='application/json')
        #response.headers['Location'] = "/books/"+str(new_book['isbn'])
        response.headers['Location'] = "/books/"+str(request_data['isbn'])
        return response
    else:
        invalidBookObjectErrorMsg = {
            "error":"Invalid book object passed in request",
            "helpString": "Data passed is similar to this {'name':'book 2','price':99.90, 'isbn':456}"
        }
        response = Response(json.dumps(invalidBookObjectErrorMsg), status=400, mimetype='application/json')
        return response


@app.route('/books/<int:myisbn>', methods=['PUT'])
def replace_book(myisbn):
    request_data = request.get_json()
    if(not valid_put_request_data(request_data)):
        invalidBookObjectErrorMsg = {
            "error":"Invalid book object passed in request",
            "helpString": "Data passed is similar to this {'name':'book 2','price':99.90}"
        }
        response = Response(json.dumps(invalidBookObjectErrorMsg), status=400, mimetype='application/json')
        return response

    #new_book = {
    #    "name": request_data['name'],
    #    "price": request_data['price'],
    #    "isbn": myisbn
    #}
    #i = 0
    #for book in books:
    #    currentIsbn = book["isbn"]
    #    if currentIsbn == myisbn:
    #        books[i] = new_book
    #    i += 1
    Book.replace_book(myisbn,request_data['name'],request_data['price'])
    response = Response("", status=204)

    return response


@app.route('/books/<int:myisbn>', methods=['PATCH'])
def patch_book(myisbn):
    request_data = request.get_json()
    updated_book = {}

    if("name" in request_data):
        #updated_book["name"]=request_data["name"]
        Book.update_book_name(myisbn, request_data['name'])
    if("price" in request_data):
        #updated_book["price"]=request_data["price"]
        Book.update_book_price(myisbn, request_data['price'])

    #for book in books:
    #    if book["isbn"] == myisbn:
    #        book.update(updated_book)
    response = Response("", status=204)
    response.headers['Location']='/books/'+str(myisbn)

    return response


@app.route('/books/<int:myisbn>', methods=['DELETE'])
def delete_book_by_isbn(myisbn):
    #i=0
    #for book in books:
    #    if book["isbn"] == myisbn:
    #        books.pop(i)
    #        response = Response("",status=204)
    #        return response
    #    i += 1

    if(Book.delete_book(myisbn)):
        response = Response("", status=204)
        return response

    invalidBookObjectErrorMsg = {
        "error":"Book with that ISBN was not found",
        "helpString": "Data passed is similar to this {'name':'book 2','price':99.90}"
    }
    response = Response(json.dumps(invalidBookObjectErrorMsg), status=404, mimetype='application/json')
    return response

