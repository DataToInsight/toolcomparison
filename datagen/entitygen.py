import string
import random
myRandom = random.SystemRandom()

# TODO: move out of entity layer, into outer layer
import csv
from itertools import chain
def csv_to_list(path):
	with open(path, 'rb') as f:
		def namereader():
			for row in csv.reader(f, delimiter=',', quotechar='"'):
				yield [item.decode("cp1252") for item in row]
		return list(chain.from_iterable(namereader()))

name_first = csv_to_list('./../inputdata/firstnames.csv')
name_last = csv_to_list('./../inputdata/lastnames.csv')
product_parts = ["Monkey", "Cat", "Dog", "Kitten", "Parrot", "Chicken", "Cow",
				 "Fun", "Loving", "Happy", "Working", "Sweet", "Soft",
				 "Big", "Bigger"]

def random_word(N):
	return ''.join(myRandom.choice(string.ascii_uppercase + string.digits) for _ in range(N))


def random_name():
	return ' '.join([myRandom.choice(name_first),
						random_word(5),
						random_word(5),
						myRandom.choice(name_last)])

def random_product_label():
	return ''.join([myRandom.choice(product_parts) for _ in range(4)]+
							 [random_word(10)])

def random_product_price():
	return pow(2,myRandom.uniform(1.5, 5))

def name_list(N):
	return [random_name() for _ in range(N)]


def random_transaction(n_persons, n_products):
	return [myRandom.randint(0, n_persons-1), # buyer
	myRandom.randint(0, n_persons-1), # seller
	myRandom.randint(0, n_products-1), # product
	myRandom.lognormvariate(0.5, 0.05) # pricefactor
	]



# name -> transaction -> product
def get_persons(n_persons):
	for i in range(n_persons):
		yield (i, random_name())


def get_products(n_prod):
	for i in range(n_prod):
		yield (i, random_product_label(), random_product_price())


def get_transactions(n_persons, n_prod, n_trans):
	for i in range(n_trans):
		yield random_transaction(n_persons, n_prod)