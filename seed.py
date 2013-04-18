import model
import csv

def load_users(session):
	# users.csv found in seed_data directory, must be ascii compliant as decoding isn't handled here
	with open('seed_data/users.txt') as f:
		reader = csv.reader(f, delimiter = "|")

		for row in reader:
			title = row
			print title
			id = title[0]
			first = title[1]
			last = title[2]
			email = title[3]
			password = title[4]
			location = title[5]

			# set kwards equal to items in dictionary 
			c = model.User(id=id, first=first, last=last, email=email, password = password, location=location)
			session.add(c)
		session.commit()


# def load_items(session):
# 	# user items.csv


# 	id = 
# 	user_id = 
# 	name = 
# 	type = 
# 	image_url = 
# 	item_rating = 

top_id = items.id(10)


def main(session):
	load_users(session)
# 	load_items()


if __name__ == "__main__":
	print "we are in seed.py"
	s = model.connect()
	main(s)