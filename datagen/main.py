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
	n_persons = 125
	n_prod = 125
	n_trans = 250
	try:
		opts, args = getopt.getopt(argv,"hn:p:t:",["persons=","products=","transactions="])
	except getopt.GetoptError:
		print 'toolcomparison.py -n <persons> -p <products> -t <transactions>'
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print 'toolcomparison.py -n <persons> -p <products> -t <transactions>'
			sys.exit()
		elif opt in ("-n", "--persons"):
			n_persons = arg
		elif opt in ("-p", "--prods"):
			n_prod = arg
		elif opt in ("-t", "--trans"):
			n_trans = arg
		else:
			print 'toolcomparison.py -n <persons> -p <products> -t <transactions>'
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
		store_persons(conn, get_persons(n_persons))
		store_products(conn, get_products(n_prod))
		store_transactions(conn, get_transactions(n_persons, n_prod, n_trans))
	finally:
		conn.close()


if __name__ == '__main__':
	main(sys.argv)