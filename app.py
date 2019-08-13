from flask import Flask, jsonify, request, Response
import json, jwt, datetime

app.config['SECRET_KEY'] = 'meow'

app = Flask(__name__)
print(__name__)

books = [
	{
		'id': 1,
		'name': 'Green Eggs and Ham',
		'price': 7.99,
		'isbn': 123456789
		
	},
	{
		'id': 2,
		'name': 'Cat in the Hat',
		'price': 6.99,
		'isbn': 987654321
	}
]

#GET /
@app.route('/')
def helloWorld():
	return 'Vini World'

#GET /
@app.route('/login')
def getToken():
	expiration_date = datetime.datetime.utcnow() + datetime.timedelta(seconds=100)
	token = jwt.encode({'exp':expiration_date}, app.config['SECRET_KEY'], algorithm='HS256')
	return token

#GET /books?token=weiwoeiwiw54wpwppp12
@app.route('/books')
def getBooks():
	token = request.args.get('token')
	try:
		jwt.decode(token, app.config['SECRET_KEY'])
	except:
		return jsonify({'error':'Invalid Auth Token'})
		
	return jsonify({'books': books})

#GET /books/isbn
@app.route('/books/<int:isbn>')
def getBookByISBN(isbn):
	returnValue = {}
	for book in books:
		if book['isbn'] == isbn:
			returnValue = {
				'name': book['name'],
				'price': book['price'],
			}
	return jsonify(returnValue)

'''
{
	"name": "Dr. Suess Next",
	"price": 5.99
}
'''

#POST a book /books
@app.route('/books', methods = ['POST'])
def addBook():
	requestData = request.get_json()
	if(isValidBook(requestData)):
		newBook = {
			"name": requestData["name"],
			"price": requestData["price"],
			"isbn": requestData["isbn"]
		}
		books.insert(0, newBook)
		response = Response("", status=201, mimetype='application/json') 
		response.headers['Location'] = "/books" + str(newBook['isbn'])
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
def putBookByISBN(isbn):
	request_data = request.get_json()
	if(not isValidUpdateBook(request_data)):
		invalidBookErrorMsg = {
			"error": "Invalid book object",
			"message": "Book data format should be 'isbn':4266227288,'name':'Book6','price':8.99}"
		}
		response = Response(json.dumps(invalidBookErrorMsg), status=400, mimetype='application/json')
		return response

	newBook = {
		'name': request_data['name'],
		'price': request_data['price'],
		'isbn': isbn
	}
	i = 0;
	for book in books:
		currentIsbn = book['isbn']
		if currentIsbn == isbn:
			books[i] = newBook
		i+=1
	response = Response("", status=204)
	return response

#PATCH /books/123456789
@app.route('/books/<int:isbn>', methods=['PATCH'])
def patchBookByISBN(isbn):
	request_data = request.get_json()
	updatedBook = {}
	if("name" in request_data):
		updatedBook["name"] = request_data['name']
	if("price" in request_data):
		updatedBook["price"] = request_data['price']
	for book in books:
		if book["isbn"] == isbn:
			book.update(updatedBook)
	response = Response("", status=204)
	response.headers['Location'] = "/books/" + str(isbn)
	return response

#DELETE /books/123456789
#Body : {'name':"Ramayan"}
@app.route('/books/<int:isbn>', methods=['DELETE'])
def deleteBookByISBN(isbn):
	i = 0
	for book in books:
		if book["isbn"] == isbn:
			books.pop(i)
			response = Response("", status=204)
			response.headers['Location'] = "/books/" + str(isbn)
			return response
		i+=1
	invalidBookErrorMsg = {
			"error": "ISBN not found", 
			"message": "Book with this ISBN not found}"
		}
	response = Response(json.dumps(invalidBookErrorMsg), status=404, mimetype='application/json')
	response.headers['Location'] = "/books/" + str(isbn)
	return response

def isValidBook(book):
	if("name" in book
			and "price" in book
				and "isbn" in book):
		return True
	else:
		return False

def isValidUpdateBook(book):
	if("name" in book
			and "price" in book):
		return True
	else:
		return False	

app.run(port=5000)

