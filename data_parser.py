import csv, pdb

conversion = {'Male':0, 'Female':1, 'Enterprise':2, 'Unknown':3, 'Madrid':0, 'Barcelona':1, 'Auto':0, 'Accomodation':1, 'Bars and restaurants':2, 'Books and press':3, 'Fashion':4, 'Food':5, 'Health':6, 'Home':7, 'Hypermarkets':8, 'Leisure':9, 'Other services':10, 'Real state':11, 'Sports and toys':12, 'Technology':13, 'Transport':14, 'Travel':15, 'Wellness and beauty':16, '<=18':10, '19-25':20, '26-35':30, '36-45':40, '46-55':50, '56-65':50, '>=66': 70}

with open('bbva_cube_sectors.csv', 'rb') as datafile:
	with open('parsedfile.csv', 'wb') as parsedfile:
		reader = csv.reader(datafile, delimiter=',', quotechar='"')
		writer = csv.writer(parsedfile, delimiter=',', quotechar='"')

		for row in reader:
			new_row = []
			for counter,field in enumerate(row):
				if field in conversion:
					new_row.append(conversion[field])
				else:
					new_row.append(field)

				try:	
					if '-' in new_row[counter]:
						new_row[counter] = new_row[counter].replace('-', '')
				except:
					pass
			writer.writerow(new_row)
