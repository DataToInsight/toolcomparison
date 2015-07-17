import os
import string
import random
from datetime import timedelta, datetime
import math
from time import sleep
from geopy.geocoders import GoogleV3
geolocator = GoogleV3()

myRandom = random.SystemRandom()

# TODO: move out of entity layer, into outer layer
import csv
from itertools import chain
def csv_to_list_chained(path):
	with open(path, 'rb') as f:
		def namereader():
			for row in csv.reader(f, delimiter=',', quotechar='"'):
				yield [item.decode("cp1252").strip()  if isinstance(item, basestring) else item for item in row]
		return list(chain.from_iterable(namereader()))


def csv_to_list(path):
	with open(path, 'rb') as f:
		def namereader():
			for row in csv.reader(f, delimiter=',', quotechar='"'):
				yield [item.decode("cp1252").strip()  if isinstance(item, basestring) else item for item in row]
		return list(namereader())

name_first = csv_to_list_chained('./../inputdata/firstnames.csv')
name_last = csv_to_list_chained('./../inputdata/lastnames.csv')
countries = csv_to_list('./../inputdata/countries.csv')

def get_geos(names):
	for n in names:
		sleep(0.4)
		print("")
		print(n)
		location = geolocator.geocode(n)
		if location is not None:
			print((location.address, location.latitude, location.longitude))
			yield (n, location.latitude, location.longitude)
		else:
			print("NO GEO FOUND: " + n)


def write_csv(f, gen):
	with open(f, 'wb') as csvfile:
		csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
		for r in gen:
			csvwriter.writerow([item.encode("cp1252") if isinstance(item, basestring) else item for item in r])

geo_path = './../inputdata/geo_countries.csv'
if not os.path.isfile(geo_path):
	write_csv(geo_path, get_geos(countries))

geo_countries = csv_to_list(geo_path)

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

def generate_matches():
	now = datetime.now()
	match_day = [(now - timedelta(days=d, seconds=now.second, microseconds=now.microsecond)) for d in range(7,21,2)]
	match_day.reverse()
	for x in range(0, len(match_day)):
		yield (''.join(["Matchday ", (1+x).__str__()]),
		match_day[x]-timedelta(hours=4),
		match_day[x]+timedelta(hours=4))


all_known_matches = generate_matches()


def random_word(N):
	return ''.join(myRandom.choice(string.ascii_uppercase + string.digits) for _ in range(N))

def random_person(id):
	name= ' '.join([myRandom.choice(name_first),
					 myRandom.choice(name_first),
						random_word(5),
						random_word(5),
						myRandom.choice(name_last)])

	country = myRandom.choice(geo_countries)
	print(country)
	return(id, name, country[0], country[1], country[2])


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


def during_match(date_time):
	for m in all_known_matches:
		if m[1] < date_time < m[2]:
			return True
	return False


def random_transaction(person1, person2, n_products):
	buyer, seller = random_flip((person1, person2))
	hour_of_day = 24*math.sin(myRandom.uniform(0, math.pi))
	day = myRandom.randint(0, 31*2)
	buy_time = 	datetime.now() - timedelta(hours=hour_of_day, days=day)
	product = myRandom.randint(0, n_products-1)
	if during_match(buy_time):
		if myRandom.uniform(0,10)<3:
			if product_parts % 3 < 2:
				buy_time = buy_time - timedelta(hours=myRandom.uniform(8, 40))
			else:
				buy_time = buy_time + timedelta(hours=myRandom.uniform(8, 40))
	return (buyer,
		seller,
		product,
		myRandom.lognormvariate(0.5, 0.05), # pricefactor
		buy_time
		)


def get_matches():
	return all_known_matches


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