import csv, pdb

conversion = {'Male':23, 'Female':24, 'Enterprise':25, 'Unknown':26, 'Madrid':1, 'Barcelona':2, 'Auto':4, 'Accomodation':5, 'Bars and restaurants':6, 'Books and press':7, 'Fashion':8, 'Food':9, 'Health':10, 'Home':11, 'Hypermarkets':12, 'Leisure':13, 'Other services':14, 'Real state':15, 'Sports and toys':16, 'Technology':17, 'Transport':18, 'Travel':19, 'Wellness and beauty':20, '<=18':10, '19-25':20, '26-35':30, '36-45':40, '46-55':50, '56-65':50, '>=66': 70}

#zipcode, madrid, barcelona, Date, auto, accomodation, Bars and restaurants, Books and press, Fashion, Food, Health, Home, Hypermarkets, Leisure, Other services, Real state, Sports and toys, Technology, Transport, Travel, Wellness and beauty, Date, Num Cards, Num Payments, Male, Female, Age Range, Avg. Sales/Month

with open('bbva_cube_sectors.csv', 'rb') as datafile:
	with open('bin_parsedfile.csv', 'wb') as parsedfile:
		reader = csv.reader(datafile, delimiter=',', quotechar='"')
		writer = csv.writer(parsedfile, delimiter=',', quotechar='"')

		writer.writerow(['zipcode', 'Madrid', 'Barcelona', 'Date', 'Auto', 'Accomodation', 'Bars and restaurants', 'Books and press', 'Fashion', 'Food', 'Health', 'Home', 'Hypermarkets', 'Leisure', 'Other services', 'Real state', 'Sports and toys', 'Technology', 'Transport', 'Travel', 'Wellness and beauty', 'Num Cards', 'Num Payments', 'Male', 'Female', 'Enterprise', 'Other', 'Age Range', 'Avg Sales'])
		next(reader, None)
		for row in reader:
			new_row = [0]*29
			#zipcode
			new_row[0] = row[0]
			#city
			new_row[conversion[row[1]]] = 1
			#date
			new_row[3] = row[2].replace('-', '')
			#sector
			new_row[conversion[row[3]]] = 1
			#Num card
			new_row[21] = row[4]
			#num payment
			new_row[22] = row[5]
			#Gender
			new_row[conversion[row[6]]] = 1
			#Age Range
			new_row[27] = conversion[row[7]]
			#Avg Sales
			new_row[28] = row[8]

			writer.writerow(new_row)
