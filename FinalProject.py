import sqlite3

connection = sqlite3.connect('finalproj.sqlite3')
cursor = connection.cursor()

cursor.execute('DROP TABLE IF EXISTS IPAddress')
cursor.execute('CREATE TABLE IPAddress(IPAddressID TEXT, IPAddressText TEXT)')
cursor.execute('DROP TABLE IF EXISTS EventMessage')
cursor.execute('CREATE TABLE EventMessage(messageID, messageText)')

def FinalProjectCode():
    
    #This function is called in every other function following it, its purpose is to take the Applog.txt file and split it into 3 sections with nodes, addresses, and messages
    def splitLog():
        sections = []
        with open('Applog.txt', 'r') as log:
            for item in log:
                section = item.split(' - ')
                sections.append(section)
        return sections
    
    #This function takes the splitlog function to seperate the sections of the Applog file, then it takes the Node and Message section and puts it into a tuple together
    #It then checks if the Data tuple is the message we are looking for, if it is it adds +1 to that node tuple in the dictionary
    #If the message we are searching for is not in the tuple, it still adds that node to the dictionary as a zero
    
    #the next section compares the values to eachother to see which node has the most values and then prints that node and value.
    def failedPayments():
        paymentsDictionary = {}
        sections = splitLog()
        for section in sections:
            readNode = section[0].strip()
            readData = section[2].strip()
            nodeDataTuple = (readNode, readData)
            if nodeDataTuple[1] == "User Failed Payment":
                paymentsDictionary[(nodeDataTuple[0])] += 1
            else:
                if nodeDataTuple[0] not in paymentsDictionary:
                    paymentsDictionary[nodeDataTuple[0]] = 0
                else:
                    continue
        mostNode = ()
        count = 0
        for key, value in paymentsDictionary.items():
            if value > count:
                mostNode = key
                count = value
        print(mostNode, count)
    
    #this function takes the splitlog function and breaks it down only to the nodes, then it checks to see if this node is in the eventsDictionary or not
    #If it is, it adds +1 to that node, if not it adds that node to the dictionary. It then prints the key and value for the nodes.
    def nodeEvents():
        eventsDictionary = {}
        sections = splitLog()
        for section in sections:
            node = section[0]
            if node in eventsDictionary:
                eventsDictionary[(node)] += 1
            else:
                eventsDictionary[(node)] = 1
        for key, value in eventsDictionary.items():
            print(key, value)
    
    #this function takes the splitlog function and breaks it down to only the IP addresses, it then splits it into only the octets, it then checks if both the first and second octet are 3 numbers long
    #if they are, it adds +1 to the IPcount and then prints that final value. I then added code to see if the address has been added to the dictionary yet.
    #If it has not, it will add it, if it has then it will add a +1 to that value.
    def ipList():
        ipCount = 0
        ipDictionary = {}
        sections = splitLog()
        for section in sections:
            address = section[1]
            octets = address.split('.')
            if len(octets[0]) == 3 and len(octets[1]) == 3:
                ipCount += 1
                if address in ipDictionary:
                    ipDictionary[(address)] += 1
                else:
                    ipDictionary[(address)] = 1
        for key, value in ipDictionary.items():
            print(key, "-", value)
            cursor = connection.cursor()
            cursor.execute("INSERT INTO IPAddress(IPAddressID, IPAddressText) VALUES(?,?)",(key, value))
            connection.commit()
            cursor.close()
        print("There are", ipCount, "three digit first octet and three digit second octet addresses")
    
    #This function asks for an input for the user to input an IP octet value to search, it then brings in the splitlog function to break it down to onlu IP addresses
    #after this it finds the first and last octet and then creates a tuple of the first octet, last octet, and full address, then it compares the user IP to the first or last octet
    #if the user IP matches either of these, it prints out the full address
    def ipSearch():
        userIP = input("Please enter an IP octet value to search for: ")
        sections = splitLog()
        for section in sections:
            address = section[1]
            firstOctetPt1 = address.find('.')
            firstOctetPt2 = address[:firstOctetPt1]
            lastOctetPt1 = address.rfind('.')
            lastOctetPt2 = address[lastOctetPt1 + 1:]
            addressTuple = (firstOctetPt2, lastOctetPt2, address)
            if userIP == addressTuple[0] or userIP == addressTuple[1]:
                print(addressTuple[2])
    
    #this function takes the splitlog function and splits it to only IP addresses, it then breaks it down to only the first octet value and then it sees if this value is in the octetsDictionary
    #If it is not, it adds it to the dictionary, if it is, it adds a +1 to that value. It then prints the octet and the number of times it is seen to the screen
    def uniqueOctets():
        octetsDictionary = {}
        sections = splitLog()
        for section in sections:
            address = section[1]
            firstOctetPt1 = address.find('.')
            firstOctetPt2 = address[:firstOctetPt1]
            if firstOctetPt2 in octetsDictionary:
                octetsDictionary[(firstOctetPt2)] += 1
            else:
                octetsDictionary[(firstOctetPt2)] = 1
        for key, value in octetsDictionary.items():
            print(key, '-', value)
    
    #this function calls the splitlog function and breaks it down to only the messages, it then checks to see if this message is in the messagesDictionary
    #if it is not, it adds it to the dictionary, if it is, it adds a +1 to that message. It then prints these values to the screen.
    def uniqueMessages():
        messagesDictionary = {}
        sections = splitLog()
        for section in sections:
            message = section[2].strip()
            if message in messagesDictionary:
                messagesDictionary[(message)] += 1
            else:
                messagesDictionary[(message)] = 1
        for key, value in messagesDictionary.items():
            cursor = connection.cursor()
            cursor.execute("INSERT INTO EventMessage(messageID, messageText) VALUES(?,?)",(key, value))
            connection.commit()
            cursor.close()
            print(key, '-', value)

    #this function only is to display a menu to the screen. It says that if the selection is not 7 then to continue to show the menu then inputs from the user a selection
    #it has an if statement for each selection and if the number is chosen then it  calls the function related to the number
    def showMenu():
        selection = ""
        while selection != "7":
            print("\n-----Select a Challenge to Solve-----")
            print("1 - Failed Payments")
            print("2 - Node Events")
            print("3 - List of IP Addresses")
            print("4 - IP Address Search")
            print("5 - Octets")
            print("6 - Unique Messages")
            print("7 - Quit")
            print("")
            selection = input("Please enter a menu number: ")
            
            if selection == '1':
                failedPayments()
            if selection == '2':
                nodeEvents()
            if selection == '3':
                ipList()
            if selection == '4':
                ipSearch()
            if selection == '5':
                uniqueOctets()
            if selection == '6':
                uniqueMessages()
            if selection == '7':
                print("End")
    
    showMenu()