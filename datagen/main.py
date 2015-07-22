import sys, getopt
import json
from datagen.database import *
from datagen.entitygen import *

import psycopg2 # TODO: move into database.py

def print_items(n_persons, n_prod, n_trans):
	print("The names:")
	names = get_persons(n_persons)
	print('\r\n'.join("%s" % (n,) for n in names))

	print("The products:")
	products = get_products(n_prod)
	print('\r\n'.join("%s"% (p,) for p in products))
	print("The transactions (name, name, product, price):")
	transactions = get_transactions(n_persons, n_prod, n_trans)
	print('\r\n'.join("%s" % (t,) for t in transactions))


def main(argv):
	# Determine how much data to generate
	#n_persons = 12500
	#n_prod = 12500
	# bol.com
	n_persons = 15E6 # bol.com has 7 million articles, and 17.5 milion transactions a year in 2011 when it had 3.4 milion customers
	n_prod = 10E6
	try:
		opts, args = getopt.getopt(argv,"hn:p:t:",["persons=","products="])
	except getopt.GetoptError:
		print 'toolcomparison.py -n <persons> -p <products>'
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print 'toolcomparison.py -n <persons> -p <products>'
			sys.exit()
		elif opt in ("-n", "--persons"):
			n_persons = arg
		elif opt in ("-p", "--prods"):
			n_prod = arg
		else:
			print 'toolcomparison.py -n <persons> -p <products>'
			sys.exit()
	# Determine where to store the data
	with open('./../config.json') as config_file:
		config = json.load(config_file)
	user = config["database"]["user"]
	pwd = config["database"]["password"]
	try:
		conn = psycopg2.connect(database='toolcomparison',
								user=user,
								password=pwd,
								host='localhost')
	except:
		print "I am unable to connect to the database"
	# Let the storage persist all data
	try:
		print("Generating matches")
		store_matches(conn, get_matches())
		print("Generating persons")
		store_persons(conn, get_persons(n_persons))
		print("Generating products")
		store_products(conn, get_products(n_prod))
		print("Generating transactions")
		store_transactions(conn, get_transactions(n_persons, n_prod))
	finally:
		conn.close()


if __name__ == '__main__':
	main(sys.argv)