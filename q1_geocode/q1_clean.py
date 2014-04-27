__author__ = 'reshamashaikh'
# --------------------------------------------------------------------------
# Date:         4/24/14
# Version:      Python 3.3
#
# Path:         /Users/reshamashaikh/_0ba/_projects/_sumall/q1_geocode
# Script:
# Description:  SumAll.org Assessment Assignment
# --------------------------------------------------------------------------


from operator import itemgetter
import time

# import function to calculate geo-distance
from f_distance import *

# https://pypi.python.org/pypi/geopy/0.99
from geopy.geocoders import GoogleV3


# set working directory
path_data = "/Users/reshamashaikh/_0ba/_projects/_sumall/q1_geocode/_data/"


print("-" * 100)


# ------------------------------
# Part 1 - read in files
# ------------------------------

# Files
# test_names.csv  --> 10,000 rows:  	resp-lsn	resp-ftn	resp-mi
# train_names.csv --> 65,533 rows:  	resp-lsn	resp-ftn	resp-mi	resp-strt-no	resp-strt	resp-apn	resp-state

#	        resp-lsn	resp-ftn	resp-mi
# 120173	FOX	OLIVIA
# 622259	GUZMAN/PERALTA	AMBER/RUDDY

# 	resp-lsn	resp-ftn	resp-mi	resp-strt-no	resp-strt	resp-apn	resp-state
# 0	LOPEZ	RUTH		829	SCHENCK AVE	03F	NY
# 1	VASQUEZ	PAULINA		829	SCHENCK AVE	02D	NY
# 2	TUUCKER	SYLVIA		829	SCHENCK AVE	01B	NY


file1 = open(path_data + 'test_names.csv', 'r')


# initialize dictionary
mydict = {}



linect=-1
maxlines = 10000 + 1
#maxlines = 10

# read file with Names and put into dictionary

for line in file1:
    linect += 1
    if linect < maxlines and linect > 0:    # skip first line since it is header
        #print("\n")
        line = line.strip()                 # remove carriage returns at end of line

        #print(line)
        #print(line.find("/"))
        if line.find("/") > -1:
            newline = line.replace('/', '_')
        elif line.find("/") == -1:
            newline = line
        #print(line)
        line = newline.split(',')
        #print(line)
        key_name = line[1] + "_" + line[2]
        #print(key_name)
        if key_name not in mydict:
            mydict[key_name] = line[0:]
        else:
            key_name = key_name + "_" + line[0]
            mydict[key_name] = line[0:]


# Check length of dictionary and sum of frequency counts
print("-" * 100)
print("file 1: ")
print("linect: ", linect)
print("len(mydict): ", len(mydict))
print('')
#print(mydict['MARTINEZ_CARMEN'])
print("sum mydict val: ", sum(map(len, mydict.values())))



print("-" * 100)

file2 = open(path_data + 'train_names.csv', 'r')

# initialize dictionary
d_address= {}
d_address_subset = {}

# create a set of unique street names; this will require less queries to the Google Maps API
streetNames = set()


linect = -1
maxlines = 1182534 + 1
#maxlines = 200
for line in file2:
    linect += 1
    if linect < maxlines and linect > 0:    # skip first line since it is header
        #print("\n")
        line = line.strip()                 # remove carriage returns at end of line

        #print(line)
        #print(line.find("/"))
        if line.find("/") > -1:
            newline = line.replace('/', '_')
        elif line.find("/") == -1:
            newline = line
        #print(line)
        line = newline.split(',')
        #print("line:")
        #print(line)
        street=line[5]
        street = street.replace("_", ' ')

        #print("street: ", linect, street)
        streetNames.add(street)
        key_name = line[1] + "_" + line[2]

        address = line[-4:]
        #print(address)
        address = address[0] + " " + address[1] + " '" + address[2] + " '" + str(address[3])
        address = address.replace("'", '')

        if key_name in mydict and key_name != 'ARON_GAL':
            mydict[key_name].extend(line[0:])
            d_address[key_name] = address
            #print(key_name, mydict[key_name])

# each entry looks like
#----------------------------------------------------------------------------------------------------
#CORBETT_CASSANDRA ['930500', 'CORBETT', 'CASSANDRA', '', '32', 'CORBETT', 'CASSANDRA', '', '872', 'ASHFORD ST', '04E', 'NY']
#RIVERA_RICHARD ['747049', 'RIVERA', 'RICHARD', '', '60', 'RIVERA', 'RICHARD', '', '720', 'BERGEN STREET', '2RF', 'NY']
#SANCHEZ_CARLOS ['179493', 'SANCHEZ', 'CARLOS', '', '116', 'SANCHEZ', 'CARLOS', '', '1493', 'GATES AVENUE', '2', 'NY']
#DECOTEAU_ALETHEA ['847692', 'DECOTEAU', 'ALETHEA', 'D', '130', 'DECOTEAU', 'ALETHEA', 'D', '75', 'MARTENSE STREET', '5-C', 'NY']
#CHAUCA_JOSE ['479208', 'CHAUCA', 'JOSE', '', '149', 'CHAUCA', 'JOSE', '', '32-30', '48TH STREET', '', 'NY']
#----------------------------------------------------------------------------------------------------


print("-" * 100)
print("file2: ")
print("linect: ", linect)
print("len(mydict): ", len(mydict))

print('')
#print(mydict['MARTINEZ_CARMEN'])

print("sum mydict val: ", sum(map(len, mydict.values())))

print("-" * 100)
print("streetNames (set): ")
print("len(streetNames)", len(streetNames))



print("-" * 100)
print("start sub search")
# initialize dictionary
d_address_subset = {}
strings_yes = ("CENTRE", "LAFAYETTE", "GRAND", "MULBERRY", "KENMARE", "CANAL", "CROSBY", "HOWARD",\
    "SPRING","PRINCE", "ELIZABETH","BOWERY","HESTER", "BROADWAY", "HOUSTON","CHRYSTIE","HOGAN",\
    "BAXTER", "FORSYTH","MERCER","GREENE", "WOOSTER","THOMPSON","WEST BROADWAY","LISPENARD","WALKER",\
    "WHITE","FRANKLIN","LEONARD","WORTH","ELDRIDGE","ALLEN","ORCHARD","THOMPSON",\
    "AMERICAS","VARICK","LAIGHT", "ERICSSON", "ST JOHN","CHURCH","LEONARD","HOGAN","BAYARD",\
    "PELL","CLEVELAND","MOTT","DIVISION","HUDSON",\
    "SULLIVAN","DOMINICK","WATTS","PEARL","LUDLOW","ESSEX","NORFOLK","SUFFOLK","DELANCEY","RIVINGTON","STANTON",\
    "BOND","GREAT JONES")

strings_no = ('GRAND CONCOURSE', 'LAFAYETTE AVE', 'GRAND CENTRAL PARKWAY', 'GRAND AVENUE', 'GRAND AVE',\
              'HOWARD AVENUE','HOWARD AVE','PARKCHESTER ROAD', "BAYCHESTER AVENUE", "CHESTER","WHITE PLAINS",\
              "FRANKLIN AVE","WADSWORTH","DODWORTH","CHANNEL","ROCKAWAY","100TH",\
              "CHURCH AVE","HENRY HUDSON","KENILWORTH")


# create subset dictionary - only add streetnames within a certain radius of home office
linect=0
for k, v in d_address.items():
    linect += 1
    #print(v)
    if any(s in v for s in strings_yes):
        #print(linect, k, v)
        if not any(sb in v for sb in strings_no):
            print("keep -->", linect, k, v)
            d_address_subset[k] = v

print("-" * 100)
print("len(d_address_subset): ", len(d_address_subset))




geolocator = GoogleV3()

# initialize dictionary - will have key, distance from office
d_dist = {}


print("-" * 100)
print("Base Address & Base Geocodes (SumAll.org office)")
base_address, (base_latitude, base_longitude) = geolocator.geocode("247 Centre Street, 6th Floor New York, NY 10013 ")
print(base_address, base_latitude, base_longitude)


print("-" * 100)
linect=-1
maxlines = 10000 + 1
#maxlines = 10

# get geocodes for subset of data

for k, v in sorted(d_address_subset.items(), key=itemgetter(0)):
    linect += 1

    if linect < maxlines:
        #print("\n")
        #print (k, v)
        address, (latitude, longitude) = geolocator.geocode(v)
        #print(address, latitude, longitude)

        dist = distance_on_unit_sphere(base_latitude, base_longitude, latitude, longitude)
        #print(dist)
        d_dist[k] = dist
        #d_address_subset[k].extend(linect)
        #mydict[key_name].extend(line[0:])
        #, address, latitude, longitude, dist)
        #print(d_dist)
        print(linect, k, address, latitude, longitude, dist)
        time.sleep(3)

print("-" * 100)
print("len(d_dist): ",len(d_dist))



print("-" * 100)

# print records, in order of shortest distance to office
keynum = 0
for k, v in sorted(d_dist.items(), key=itemgetter(1)):
    keynum += 1
    if keynum < 25:
        print(keynum, "\t", k,"\t\t\t", v)



exit()








