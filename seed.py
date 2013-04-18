import model
import csv

def load_users(session):
	# users.csv found in seed_data directory, must be ascii/UTF-8 compliant as decoding isn't handled here
	with open('seed_data/users.txt') as f:
		reader = csv.reader(f, delimiter = "|")

		# data format - ['1', 'Chris', 'Meono', 'meonocr@ucla.edu', 'pass', '90291']
		for row in reader:
			print row
			id = row[0]
			first = row[1]
			last = row[2]
			email = row[3]
			password = row[4]
			location = row[5]

			# Use kwargs to create dictionary with row item - ({'last': 'Meono', 'id': '1', 'location': '90291', 'password': 'pass', 'email': 'meonocr@ucla.edu', 'first': 'Chris'}). Note this creates a list of dictionaries, zips __init__ kwargs with row values 
			c = model.User(id=id, first=first, last=last, email=email, password = password, location=location)
			session.add(c)
		session.commit()


# def load_items(session):
# 	# items.csv found in seed_data directory, must be ascii/UTF-8 compliant as decoding isn't handled here
# 	with open('seed_data/items.txt') as f:
# 		reader = csv.reader(f, delimiter = "|")

# 		for row in reader:
# 			print row
# 			id = row[0]
# 			user_id = row[1]
# 			name = row[2]
# 			type = row[3]
# 			tag = row[4]
# 			image_url = row[5]
# 			color = row[6]
# 			item_rating = row[7]

# 			c = model.User(id=id, user_id=user_id, name=name, type=type, tag=tag, image_url=image_url, color=color, item_rating=item_rating)
# 			session.add(c)
# 		session.commit()

# def load_outfits(session):
# 	# outfits.csv found in seed_data directory, must be ascii/UTF-8 compliant as decoding isn't handled here
# 	with open('seed_data/outfits.txt') as f:
# 		reader = csv.reader(f, delimiter = "|")

# 		for row in reader:
# 			print row
# 			id = row[0]
# 			user_id = row[1]
# 			top_id = row[2]
# 			bottom_id = row[3]
# 			dress_id = row[4]
# 			shoes_id = row[5]
# 			jewelry_id = row[6]
# 			accessories_id = row[7]
# 			outfit_rating = row[8]

# 			c = model.User(id=id, user_id=user_id, top_id=top_id, bottom_id=bottom_id, dress_id=dress_id, shoes_id=shoes_id, jewelry_id=jewelry_id, accessories_id=accessories_id, outfit_rating=outfit_rating)
# 			session.add(c)
# 		session.commit()	



def main(session):
	load_users(session)
 	# load_items(session)
 	# load_outfits(session)


if __name__ == "__main__":
	print "we are in seed.py"
	s = model.connect()
	main(s)