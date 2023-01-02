# Student Name: Ashton Burke
# Student ID: 010071775


import datetime
import csv


# Source:
# got this hashmap from Joe James on YouTube sent in an email from CI
# link to video: https://www.youtube.com/watch?v=9HFbhPscPU0
# Assigns keys to values and stores them in a list/array
# utilizes loadPackages function to store all data parameters of a package into hashmap
# Time complexity of O(n)
class HashMap:
    def __init__(self):
        self.size = 39
        self.map = [None] * self.size

    # equation to determine hash key
    def _get_hash(self, key):
        hash = 0
        for char in str(key):
            hash += ord(char)
        return hash % self.size

    # time-complexity of O(1)
    # adds a key-value pair to the hashmap
    def add(self, key, value):
        key_hash = self._get_hash(key)
        key_value = [key, value]

        if self.map[key_hash] is None:
            self.map[key_hash] = list([key_value])
            return True
        else:
            for pair in self.map[key_hash]:
                if pair[0] == key:
                    pair[1] = value
                    return True
            self.map[key_hash].append(key_value)
            return True

    # time-complexity of O(1)
    # searches for key and if it exists, returns key-value
    def get(self, key):
        key_hash = self._get_hash(key)
        if self.map[key_hash] is not None:
            for pair in self.map[key_hash]:
                if pair[0] == key:
                    return pair[1]
        return None

    # time-complexity of O(1)
    # searches for a key and if it exists, key-value is popped off the list
    def delete(self, key):
        key_hash = self._get_hash(key)

        if self.map[key_hash] is None:
            return False
        for i in range(0, len(self.map[key_hash])):
            if self.map[key_hash][i][0] == key:
                self.map[key_hash].pop(i)
                return True
        return False


# assigns hashmap to object
myHash = HashMap()


# Truck class constructor
class Truck:

    def __init__(self, load, packages, miles, holding_cap, time_to_depart, speed, address):
        self.load = load
        self.packages = packages
        self.miles = miles
        self.holding_cap = holding_cap
        self.time_to_depart = time_to_depart
        self.time = time_to_depart
        self.speed = speed
        self.address = address

    def __str__(self):
        return "%s, %s, %s, %s, %s, %s, %s" % \
            (self.load, self.packages, self.miles, self.holding_cap, self.time_to_depart, self.speed, self.address)


# Package class constructor
class Package:
    def __init__(self, package_id, address, city, state, zipcode, deadline, weight, status):
        self.package_id = package_id
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.deadline = deadline
        self.weight = weight
        self.status = status
        self.departure = None
        self.delivery_time = None

    def __str__(self):
        return "%s, %s, %s, %s, %s, %s, %s, %s, %s" % (self.package_id, self.address,
                                                       self.city, self.state, self.zipcode, self.deadline, self.weight,
                                                       self.delivery_time, self.status)

    # updates status of package based on which parameter is in use
    def package_status(self, timeconversion):
        if self.departure > timeconversion:
            self.status = "On the way!"
        elif self.delivery_time < timeconversion:
            self.status = "Delivered!"
        else:
            self.status = "Waiting for departure"


# CSV file reader function
# Reads package file and stores data to a list
with open("csv files/WGUPSPackageFile1.csv", encoding='utf-8-sig') as packageFile:
    reader = csv.reader(packageFile)
    reader = list(reader)


# assigns data to package parameters and then moves package and its respective data to the hashmap
# time complexity of O(n)
def loadPackage(fileName, myHash):
    with open(fileName) as packages:
        packageData = csv.reader(packages)
        for pack in packageData:
            packID = int(pack[0])
            packAddress = pack[1]
            packCity = pack[2]
            packState = pack[3]
            packZip = pack[4]
            packDeadline = pack[5]
            packWeight = pack[6]
            packageLoadStatus = "Loaded"
            # packageTime = " "
            # sets parameters of loaded package
            pack = Package(packID, packAddress, packCity, packState, packZip, packDeadline, packWeight,
                           packageLoadStatus)
            # adds package to hashmap
            myHash.add(packID, pack)


# merges package data with hashmap
loadPackage("csv files/WGUPSPackageFile1.csv", myHash)
"""
for i in range(len(myHash.map) + 1):
    print("{},{}".format(i + 1, myHash.get(i + 1)))
"""
# CSV file reader function
# Reads package file and stores data to a list
with open("csv files/WGUPSAddressFile1.csv") as addressFile:
    addressReader = csv.reader(addressFile)
    addressReader = list(addressReader)
# CSV file reader function
# Reads package file and stores data to a list
with open('csv files/WGUPSDistanceTable1.csv') as distanceFile:
    distanceReader = csv.reader(distanceFile, delimiter=',')
    distanceReader = list(distanceReader)


# function that calculates the distance between two separate locations
# time complexity of O(1)
def deliver_distance(row, column):
    deliverDistance = distanceReader[row][column]
    if deliverDistance == '':
        deliverDistance = distanceReader[column][row]

    return float(deliverDistance)


# returns address number from address data
# time complexity of O(n)
def getAddress(address):
    for row in addressReader:
        if address in row[2]:
            return int(row[0])


# forms the loaded truck objects
# manually loads trucks with packages and sets their respective dispatch time
loadtruck1 = Truck(None, [30, 10, 11, 17, 21, 40, 31, 2, 37, 6], 0.0, 16,
                   datetime.timedelta(hours=9, minutes=5), 18,
                   "4001 South 700 East")

loadtruck2 = Truck(None, [3, 14, 16, 18, 19, 20, 29, 36, 38, 6, 34, 1, 13, 15], 0.0, 16,
                   datetime.timedelta(hours=8), 18,
                   "4001 South 700 East")

loadtruck3 = Truck(None, [9, 25, 28, 22, 32, 33, 23, 35, 24, 39, 26, 27, 4, 5, 7, 12, 8], 0.0, 16,
                   datetime.timedelta(hours=10, minutes=20), 18,
                   "4001 South 700 East")


# delivery function that utilizes the nearest neighbor algorithm
# stores all undelivered packages into an array then sets them to a loaded truck in order of the nearest address
# time complexity of O(N^2)
def delivery(truck):
    # all packages awaiting delivery
    awaiting_delivery = []
    for packageID in truck.packages:
        pkg = myHash.get(packageID)
        awaiting_delivery.append(pkg)
    # clear list for the resort by closest address
    del truck.packages[:]
    # while there are still packages awaiting delivery, deliver package to address and record delivery time data
    while len(awaiting_delivery) > 0:
        addy = 100
        packy = None
        # for every package awaiting delivery, if truck and package address is less than or equal next address
        # then deliver package
        for pkg in awaiting_delivery:
            if deliver_distance(getAddress(truck.address),
                                getAddress(pkg.address)) <= addy:
                addy = deliver_distance(getAddress(truck.address),
                                        getAddress(pkg.address))
                packy = pkg
        # sets nearest address for delivery
        truck.packages.append(packy.package_id)
        # bumps the same package from awaiting delivery list
        awaiting_delivery.remove(packy)
        # records miles traveled to address
        truck.miles += addy
        # resets trucks address after delivery to just delivered packages address
        truck.address = packy.address
        # records time of at time of delivery
        truck.time += datetime.timedelta(hours=addy / 18)
        # sets delivery time of next pacakge to trucks time
        packy.delivery_time = truck.time
        packy.departure = truck.time_to_depart


# calls for the loading of the packages to their respective trucks
delivery(loadtruck1)
delivery(loadtruck2)
# prevents truck 3 from departing until at least one of the first trucks has completed their delivery
loadtruck3.depart_time = min(loadtruck1.time, loadtruck2.time)
# once a truck has finished, loads truck 3
delivery(loadtruck3)


# sets up the user console to access package delivery data
class Interface:
    print("Welcome to WGU's Parcel Service where your parcels are our service!\n")
    print("Total truck mileage for delivery route is:\n")
    # adds the total miles traveled of each truck
    print(loadtruck1.miles + loadtruck2.miles + loadtruck3.miles)
    print("\n")
    # prompts the user for console input
    promptText = input(
        "\nPlease enter 'total' for total packages or 'single' for a specific package where you will then be prompted "
        "for the package ID number.\n\nEnter 'exit' at any point to exit the program:\n")
    # if "total" is typed, asks for time of delivery data to be pulled
    # then pulls delivery data at requested time
    if promptText == "total":
        try:
            promptTime = input("Enter time to check delivery status of all packages. TIME FORMAT: HH:MM:SS: ")
            # creates the format for users time input
            (hour, minute, second) = promptTime.split(":")
            # uses timeconversion object to set format of the object
            timeconversion = datetime.timedelta(hours=int(hour), minutes=int(minute), seconds=int(second))
            # for each package, get package ID from hash table then convert inputed time to package status and print
            for packageID in range(1, 41):
                pkg = myHash.get(packageID)
                pkg.package_status(timeconversion)
                print(str(pkg))
            # If input does not match requested input then program closes
        except ValueError:
            print("Incorrect input. Now exiting...")
            exit()
            # else if user inputs "single" asks for time of delivery data to be pulled
    elif promptText == "single":
        try:
            promptTime = input("Enter time to check delivery status of the package. TIME FORMAT: HH:MM:SS: ")
            # creates the format for users time input
            (hour, minute, second) = promptTime.split(":")
            # uses timeconversion object to set format of the object
            timeconversion = datetime.timedelta(hours=int(hour), minutes=int(minute), seconds=int(second))
            # asks for package ID in order to retrieve respective packages delivery data
            promptID = input("Enter the package ID number: ")
            # gets package ID from hash table then convert inputed time to package status and prints
            pkg = myHash.get(int(promptID))
            pkg.package_status(timeconversion)
            print(str(pkg))
            # If input does not match requested input then program closes
        except ValueError:
            print("Incorrect input. Now exiting...")
            exit()
    else:
        exit()
