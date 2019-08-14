from flask import Flask, jsonify, request, Response
from bookmodel import *
from settings import *
import json, jwt, datetime
from usermodel import BookUser
from functools import wraps

app.config['SECRET_KEY'] = 'meow'

#GET /
@app.route('/')
def helloWorld():
	return 'Vini Book World'

#GET /
@app.route('/login', methods=['POST'])
def getToken():
	request_data = request.get_json()
	username = request_data['username']
	password = request_data['password']
	isValidLogin = BookUser.validateLogin(username, password)
	
	if isValidLogin:
		expiration_date = datetime.datetime.utcnow() + datetime.timedelta(seconds=100)
		token = jwt.encode({'exp':expiration_date}, app.config['SECRET_KEY'], algorithm='HS256')
		return token
	else:
		return Response('', status=401, mimetype='application/json')

def token_required(f):
	def wrapper(*args, **kargs):
		token = request.args.get('token')
		try:
			jwt.decode(token, app.config['SECRET_KEY'])
			return f(*args, **kargs)
		except:
			return jsonify({'error':'Invalid Auth Token OR token not passed'})
	return wrapper

#GET /books?token=weiwoeiwiw54wpwppp12
@app.route('/books')
@token_required
def getBooks():
	'''	token = request.args.get('token')
	try:
		jwt.decode(token, app.config['SECRET_KEY'])
	except:
		return jsonify({'error':'Invalid Auth Token'})
	'''		
	return jsonify({'books': Book.get_all_books()})

#GET /books/isbn
@app.route('/books/<int:isbn>')
@token_required
def getBookByISBN(isbn):
	returnValue = Book.get_book_by_isbn(isbn)
	return jsonify(returnValue)

'''
{
	"name": "Dr. Suess Next",
	"price": 5.99
}
'''

#POST a book /books
@app.route('/books', methods = ['POST'])
@token_required
def addBook():
	requestData = request.get_json()
	if(isValidNewBook(requestData)):
		Book.add_book(requestData['name'], requestData['price'], requestData['isbn'])
		response = Response("", status=201, mimetype='application/json') 
		response.headers['Location'] = "/books" + str(requestData['isbn'])
		return response
	else:
		invalidBookErrorMsg = {
			"error": "Invalid book object",
			"message": "Book data format should be {'isbn':4266227288,'name':'Book6','price':8.99}"
		}
		response = Response(json.dumps(invalidBookErrorMsg), status=400, mimetype='application/json')
		return response

#PUT /books/123456789
@app.route('/books/<int:isbn>', methods=['PUT'])
@token_required
def replaceBookByISBN(isbn):
	request_data = request.get_json()
	if(not isValidReplaceBook(request_data)):
		invalidBookErrorMsg = {
			"error": "Invalid book object",
			"message": "Book data format should be 'isbn':4266227288,'name':'Book6','price':8.99}"
		}
		response = Response(json.dumps(invalidBookErrorMsg), status=400, mimetype='application/json')
		return response

	Book.replace_book(isbn, request_data['name'], request_data['price'])
	response = Response("", status=204)
	return response

#PATCH /books/123456789
@app.route('/books/<int:isbn>', methods=['PATCH'])
@token_required
def updateBookByISBN(isbn):
	request_data = request.get_json()
	if(not isValidUpdateBook(request_data)):
		invalidBookErrorMsg = {
			"error": "Invalid book object",
			"message": "Book data format should be {'name':'Book6'} OR {'price':8.99}"
		}
		response = Response(json.dumps(invalidBookErrorMsg), status=400, mimetype='application/json')
		return response

	if("name" in request_data):
		Book.update_book_name(isbn, request_data['name'])
	if("price" in request_data):
		Book.update_book_price(isbn, request_data['price'])

	response = Response("", status=204)
	response.headers['Location'] = "/books/" + str(isbn)
	return response

#DELETE /books/123456789
#Body : {'name':"Ramayan"}
@app.route('/books/<int:isbn>', methods=['DELETE'])
@token_required
def deleteBookByISBN(isbn):
	if(Book.delete_book_by_isbn(isbn)):
		response = Response("", status=204)
		return response

	invalidBookErrorMsg = {
			"error": "ISBN not found", 
			"message": "Book with this ISBN not found}"
		}
	response = Response(json.dumps(invalidBookErrorMsg), status=404, mimetype='application/json')
	return response

def isValidNewBook(book):
	if("name" in book
			and "price" in book
				and "isbn" in book):
		return True
	else:
		return False

def isValidReplaceBook(book):
	if("name" in book
			and "price" in book):
		return True
	else:
		return False	

def isValidUpdateBook(book):
	if("name" in book
			or "price" in book):
		return True
	else:
		return False

app.run(port=5000)

