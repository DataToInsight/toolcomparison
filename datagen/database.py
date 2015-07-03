

def store_names(conn, generator):
	cur = conn.cursor()
	try:
		try:
			cur.execute("""DROP TABLE IF EXISTS names CASCADE""")
			cur.execute("""DROP TABLE IF EXISTS persons CASCADE""")
		except:
			print "Failed to drop old names table"
		conn.commit()
		try:
			cur.execute("""CREATE TABLE persons (
			id integer constraint names_PK primary key,
			name TEXT
			);""")
		except:
			print "Failed to create persons table"
		conn.commit()
		for n in generator:
			cur.execute("""INSERT INTO persons(id, name) VALUES(%s, %s)""", n)
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
			price double precision
			);""")
		except:
			print "Failed to create product table"
		conn.commit()
		for n in generator:
			cur.execute("""INSERT INTO products(id, label, price) VALUES(%s, %s, %s)""", n)
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
				price_factor double precision
				);""")
		except:
			print "Failed to create transaction table"
		conn.commit()
		for n in generator:
			cur.execute("""INSERT INTO transactions(persons_id_buyer, persons_id_seller, products_id, price_factor) VALUES(%s, %s, %s, %s)""", n)
		conn.commit()
	finally:
		cur.close()