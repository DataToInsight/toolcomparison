

def store_persons(conn, generator):
	cur = conn.cursor()
	try:
		try:
			cur.execute("""DROP TABLE IF EXISTS persons CASCADE""")
		except:
			print "Failed to drop old names table"
		conn.commit()
		try:
			cur.execute("""CREATE TABLE persons (
			id integer constraint names_PK primary key,
			name TEXT,
			country TEXT,
			latitude double precision,
			longitude double precision
			);""")
		except:
			print "Failed to create persons table"
		conn.commit()
		for n in generator:
			cur.execute("""INSERT INTO persons(id, name, country, latitude, longitude) VALUES(%s, %s, %s, %s, %s)""", n)
		conn.commit()
	finally:
		cur.close()


def store_products(conn, generator):
	cur = conn.cursor()
	try:
		try:
			cur.execute("""DROP TABLE IF EXISTS products CASCADE""")
		except:
			print "Failed to drop old product table"
		conn.commit()
		try:
			cur.execute("""CREATE TABLE products (
			id integer constraint products_PK primary key,
			label TEXT,
			price double precision,
			category TEXT
			);""")
		except:
			print "Failed to create product table"
		conn.commit()
		for n in generator:
			cur.execute("""INSERT INTO products(id, label, price, category) VALUES(%s, %s, %s, %s)""", n)
		conn.commit()
	finally:
		cur.close()


def store_transactions(conn, generator):
	cur = conn.cursor()
	try:
		try:
			cur.execute("""DROP TABLE IF EXISTS transactions CASCADE""")
		except:
			print "Failed to drop old transaction table"
		conn.commit()
		try:
			cur.execute("""CREATE TABLE transactions (
				persons_id_buyer integer REFERENCES persons(id) ,
				persons_id_seller integer REFERENCES persons(id),
				products_id integer REFERENCES products(id),
				price_factor double precision,
				moment timestamp
				);""")
		except:
			print "Failed to create transaction table"
		conn.commit()
		for n in generator:
			cur.execute("""INSERT INTO transactions(persons_id_buyer, persons_id_seller, products_id, price_factor, moment) VALUES(%s, %s, %s, %s, %s)""", n)
		conn.commit()
	finally:
		cur.close()

def store_matches(conn, generator):
	cur = conn.cursor()
	try:
		try:
			cur.execute("""DROP TABLE IF EXISTS matches CASCADE""")
		except:
			print "Failed to drop old matches table"
		conn.commit()
		try:
			cur.execute("""CREATE TABLE matches (
				label TEXT,
				start timestamp,
				finish timestamp
				);""")
		except:
			print "Failed to create matches table"
		conn.commit()
		for n in generator:
			cur.execute("""INSERT INTO matches(label, start, finish) VALUES(%s, %s, %s)""", n)
		conn.commit()
	finally:
		cur.close()