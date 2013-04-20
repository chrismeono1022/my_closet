import model
import csv

def load_users(session):
	# users.txt and other seed files are in seed_data directory, must be ascii/UTF-8 compliant as decoding isn't handled here
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


def load_items(session):
	with open('seed_data/items.txt') as f:
		reader = csv.reader(f, delimiter = "|")

		for row in reader:
			print row
			id = row[0]
			user_id = row[1]
			name = row[2]
			type = row[3]
			style = row[4]
			image_url = row[5]
			color = row[6]
			item_rating = row[7]
			rain = row[8]
			heat = row[9]
			snow = row[10]
			low_temp = row[11]
			high_temp = row[12]

			c = model.Item(id=id, user_id=user_id, name=name, type=type, style=style, image_url=image_url, color=color, item_rating=item_rating, rain=rain, heat=heat, snow=snow, low_temp=low_temp, high_temp=high_temp)
			session.add(c)
		session.commit()

def load_outfits(session):
	with open('seed_data/outfits.txt') as f:
		reader = csv.reader(f, delimiter = "|")

		for row in reader:
			print row
			id = row[0]
			user_id = row[1]
			outfit_name = row[2]
			top_id = row[3]
			bottom_id = row[4]
			dress_id = row[5]
			outerwear_id = row[6]
			shoes_id = row[7]
			jewelry_id = row[8]
			accessories_id = row[9]
			outfit_rating = row[10]

			c = model.Outfit(id=id, user_id=user_id, outfit_name=outfit_name, top_id=top_id, bottom_id=bottom_id, dress_id=dress_id, outerwear_id = outerwear_id, shoes_id=shoes_id, jewelry_id=jewelry_id, accessories_id=accessories_id, outfit_rating=outfit_rating)
			session.add(c)
		session.commit()	


def main(session):
	#load_users(session)
 	load_items(session)
 	load_outfits(session)


if __name__ == "__main__":
	print "we are in seed.py"
	s = model.session
	main(s)