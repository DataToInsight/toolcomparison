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
				yield [item.decode("cp1252").strip() for item in row]
		return list(chain.from_iterable(namereader()))

name_first = csv_to_list('./../inputdata/firstnames.csv')
name_last = csv_to_list('./../inputdata/lastnames.csv')
countries = csv_to_list('./../inputdata/countries.csv')

adjective = ["Happy", "Sad", "Poor", "Joyful", "Enlightened", "Ugly", "Beautiful", "Sleepy", "Fat", "Active", "Big", "Tiny", "Sleepy", "Silent", "Noisy", "Talky", "Whispering",
			 "Drunk", "Sober", "Stoned", "Athletic", "Workaholic", "Lazy", "Travelling", "Unemployed", "Dizzy", "Productive", "Slim", "Tall", "Short",
			 "Fun", "Loving", "Happy", "Working", "Sweet", "Soft", "Bigger"]

adjective2 = {"African" : "Africa",
			  "European" : "Europe",
			  "Asian" : "Asia",
			  "Dutch" : "Europe",
			  "NorthAmerican" : "Europe",
			  "Greek" : "Europe?",
			  "Italian" : "Europe",
			  "German" : "Europe",
			  "Venezuelean" : "Latin-America",
			  "Bolivian" : "Latin-America",
			  "Belgian" : "Europe",
			  "Spanish" : "Europe",
			  "Colombian" : "Latin-America",
			  "Brazilian" : "Latin-America",
			  "Argentinian" : "Latin-America",
			  "Peruvian" : "Latin-America",
			  "Chinese" : "Asia",
			  "Chilian" : "Latin-America",
			  "Japanese" : "Asia",
			  "Mexican" : "Latin-America",
			  "United States" : "America",
			  "Canadian" : "America",
			  "Arctic" : "Cold",
			  "Antarctic" : "Cold",
			  "Korean" : "Asia",
			  "Australian" : "Austrasia",
			  "Portugese" : "Europe",
			  "Irish" : "Europe",
			  "Swedish" : "Europe",
			  "Finish" : "Europe",
			  "Norwegian" : "Europe",
			  "Danish" : "Europe"}

product_parts = ["Monkey", "Cat", "Dog", "Kitten", "Parrot", "Chicken", "Cow", "Kangaroo", "Sheep", "Sparrow", "Bird",
				 "Lion", "Tiger", "Zebra", "Giraffe", "Crocodile", "Piranha", "Penguin", "Snake", "Pig", "Whale", "Dolphin",
				 "Kibbling", "Haring", "Rabbit", "Snail", "Ostrich" , "Puma", "Gorilla", "Unicorn"
				 ]


events = [""]
def random_word(N):
	return ''.join(myRandom.choice(string.ascii_uppercase + string.digits) for _ in range(N))


def random_person(id):
	name= ' '.join([myRandom.choice(name_first),
					 myRandom.choice(name_first),
						random_word(5),
						random_word(5),
						myRandom.choice(name_last)])
	country = myRandom.choice(countries)
	return(id, name, country)


def random_product(id):
	country = myRandom.choice(adjective2.keys())
	category = adjective2[country] # value
	if myRandom.randint(0,10) < 1:
		category = None

	label = ''.join([myRandom.choice(adjective) for _ in range(2)] +
					[country] +
					[myRandom.choice(product_parts)] +
					[random_word(10)])
	price = pow(2,myRandom.uniform(1.5, 5))
	return (id, label, price, category)

def random_flip(flipped_tuple):
	if myRandom.choice( [True, False] ):
		return flipped_tuple
	else:
		return flipped_tuple[1], flipped_tuple[0]


def random_transaction(person1, person2, n_products):
	buyer, seller = random_flip((person1, person2))
	return [buyer,
		seller,
		myRandom.randint(0, n_products-1), # product
		myRandom.lognormvariate(0.5, 0.05) # pricefactor
		]


# name -> transaction -> product
def get_persons(n_persons):
	for i in range(n_persons):
		yield random_person(i)


def get_products(n_prod):
	for i in range(n_prod):
		# random null for category
		yield random_product(i)


def get_transactions(n_persons, n_prod, n_trans):
	for person1 in range(n_persons):
		if(person1>0):
			# randomly choose degree between 1 and 3
			degree = myRandom.randint(1,3)
			for j in range(degree):
				person2 = myRandom.randint(0, person1-1)
				yield random_transaction(person1, person2, n_prod)