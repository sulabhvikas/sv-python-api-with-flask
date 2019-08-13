def isValidBook(book):
	if("name" in book
			and "price" in book
				and "isbn" in book):
		return True
	else:
		return False

validBookRequest = {
	"name": "Book1",
	"price": 4.99,
	"isbn": 7666227288
}

missingISBNRequest = {
	"name": "Book2",
	"price": 3.99
}

missingNameRequest = {
	"price": 3.99,
	"isbn": 7666227288
}

missingPriceRequest = {
	"name": "Book3",
	"isbn": 7666227288
}