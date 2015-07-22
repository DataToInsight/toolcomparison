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

adjective2 = {"America" : [ "NorthAmerican", "UnitedStates", "Canadian"],
			  "Austrasia" : ["Asian", "Chinese", "Japanese", "Korean", "Australian"],
			  "Europe" : ["European", "Dutch", "Greek", "Italian", "German", "Belgian", "Spanish", "Portugese", "Irish",  "Swedish", "Finnish", "Norwegian", "Danish" ],
			 "Latin-America" : ["Venezuelean", "Bolivian", "Colombian", "Brazilian", "Argentinian", "Peruvian", "Chilian", "Mexican"]
			}
adjective2_keys = list(adjective2.keys())

product_parts = ["Monkey", "Cat", "Dog", "Kitten", "Parrot", "Chicken", "Cow", "Kangaroo", "Sheep", "Sparrow", "Bird",
				 "Lion", "Tiger", "Zebra", "Giraffe", "Crocodile", "Piranha", "Penguin", "Snake", "Pig", "Whale", "Dolphin",
				 "Kibbling", "Haring", "Rabbit", "Snail", "Ostrich" , "Puma", "Gorilla", "Unicorn"
				 ]

def generate_matches():
	now = datetime.now()
	match_day = [(now - timedelta(days=d, seconds=now.second, microseconds=now.microsecond)) for d in range(7,22,2)]
	match_day.reverse()
	for x in range(0, len(match_day)):
		yield (''.join(["Matchday ", (1+x).__str__()]),
		match_day[x]-timedelta(hours=4),
		match_day[x]+timedelta(hours=4))


all_known_matches = list(generate_matches())


def random_word(N):
	return ''.join(myRandom.choice(string.ascii_uppercase + string.digits) for _ in range(N))

def random_person(id):
	name= ' '.join([myRandom.choice(name_first),
					 myRandom.choice(name_first),
						random_word(5),
						random_word(5),
						myRandom.choice(name_last)])

	country = myRandom.choice(geo_countries)
	# Estimate
	# 111,111 * cos(latitude) meters in the x direction is 1 degree (of longitude).
	# 111,111 meters (111.111 km) in the y direction is 1 degree (of latitude)
	longitude = float(country[1])
	latitude = float(country[2])
	# offset the location with sigma of 5 km
	dx =  myRandom.normalvariate(0, 10.0) / 111.111 * math.cos(math.radians(latitude))
	dy = myRandom.normalvariate(0, 10.0) / 111.111
	return(id, name, country[0], longitude + dx, latitude+dy)


def random_product(id):
	allowed_keys = [adjective2_keys[d] for d in range(id % 3, len(adjective2_keys), 3)] # id % 3 will be equal to key_index % 3
	category = myRandom.choice(allowed_keys)
	country = myRandom.choice(adjective2[category])
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
		if m[1] <= date_time <= m[2]:
			return True
	return False


def random_transaction(person1, person2, n_products):
	buyer, seller = random_flip((person1, person2))
	hour_of_day = 24*math.sin(myRandom.uniform(0, math.pi))
	day = myRandom.randint(0, 27)
	buy_time = 	datetime.now() - timedelta(hours=hour_of_day, days=day)
	product = myRandom.randint(0, n_products-1)
	price_factor = 1
	if during_match(buy_time):
		if product % 3 < 2 and myRandom.uniform(0, 10) <= 7:
			price_factor = myRandom.lognormvariate(0, 0.1)
			if product % 3 == 0:
				buy_time = buy_time - timedelta(hours=myRandom.uniform(8, 16))
			else:
				buy_time = buy_time + timedelta(hours=myRandom.uniform(8, 16))
				price_factor = myRandom.lognormvariate(0.7, 0.05)
	else:
		myRandom.lognormvariate(0, 0.01)
	return (buyer,
		seller,
		product,
		price_factor, # pricefactor
		buy_time
		)


def get_matches():
	return all_known_matches


# name -> transaction -> product
def get_persons(n_persons):
	for i in range(int(n_persons)):
		yield random_person(i)


def get_products(n_prod):
	for i in range(int(n_prod)):
		# random null for category
		yield random_product(i)


def get_transactions(n_persons, n_prod):
	for person1 in range(int(n_persons)):
		if(person1>0):
			# randomly choose degree
			degree = myRandom.randint(1,4)
			for j in range(degree):
				person2 = myRandom.randint(0, person1-1)
				yield random_transaction(person1, person2, n_prod)