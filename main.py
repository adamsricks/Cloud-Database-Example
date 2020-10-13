import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os
from os import system, name
import glob
import json


# initializes firestore (duh)
def initialize_firestore():
    """
    Create database connection
    """

    # Your private key reference and projectId will go here
    cred = credentials.Certificate("private key.json")
    firebase_admin.initialize_app(cred, {
        'projectId': 'cloud-database-example'
    })

    # Get reference to database
    db = firestore.client()
    return db

# clears console window
def clear():
    # for windows 
    if name == 'nt': 
        _ = system('cls') 
  
    # for mac and linux(here, os.name is 'posix') 
    else: 
        _ = system('clear') 

# prints options
def printOptions():
    print("See all customers (sc)")
    print("Add customer (ac)")
    print("Edit customer (ec)")
    print("Delete customer (dc)")
    print("See all orders (so)")
    print("Add order (ao)")
    print("Edit order (eo)")
    print("Delete order (do)")
    print()
    print("Clear screen (c)")
    print("Exit (q)")

# prints all fields in a document
def printFields(db, collection, document):
    doc = db.collection(collection).document(document)
    doc = doc.get().to_dict()
    # print(f'{doc.to_dict()}')
    for f in doc:
        print("{} => {}".format(f, doc[f]))
        print()

# prints all documents in a collection
def printDocuments(db, collection):
    docList = db.collection(collection).stream()
    print()
    for doc in docList:
        # print(f'{doc.id} => {doc.to_dict()}')
        print(f'{doc.id}')

# prints all customer details
def printCustomerDetails(db, name):
    doc = db.collection("customers").document(name).get()
    doc = doc.to_dict()
    for f in doc:
        print("{} => {}".format(f, doc[f]))
        print()

# prints all customers
def printCustomers(db):
    collection = "customers"
    printDocuments(db, collection)

# create new customer
def addCustomer(db):
    print("What is the name of your new customer?")
    name = input("> ")
    print("What is the location of your new customer?")
    location = input("> ")
    print("What is the phone number of your new customer?")
    phone = input("> ")
    db.collection("customers").document(name).set({"name" : name, "location" : location, "phone" : phone})

# edit customer details
def editCustomer(db):
    print("Which customer would you like to edit?")
    name = input("> ")
    if (db.collection("customers").document(name).get().exists):
        print()
        printCustomerDetails(db, name)
        print()
        print("Which field would you like to edit?")
        print()
        field = input("> ")
        while field == "name":
            print("Cannot change name; must make new customer file")
            print("Which field would you like to edit?")
            print()
            field = input("> ")
        while field != "location" and field != "phone":
            print("Field not valid")
            print("Which field would you like to edit?")
            print()
            field = input("> ")
        print()
        print("What would you like the new field to read?")
        change = input("> ")
        db.collection("customers").document(name).set({field : change}, merge=True)
        print("Edit successful")
    else:
        print("Customer does not exist")


# deletes customer
def delCustomer(db):
    print("Which customer would you like to delete?")
    name = input("> ") 
    print("Are you sure you want to delete this customer? (y/n)")
    yon = input("> ")
    if yon == "y":
        if (db.collection("customers").document(name).get().exists):
            db.collection("customers").document(name).delete()
        else:
            print("Customer does not exist")
    else:
        print("Customer not deleted")


# prints all orders
def printOrders(db):
    num = 1
    collection = "orders"
    docList = db.collection(collection).stream()
    print("# {:<14} {:<14} {:<14}".format("Name", "Location", "Time"))
    for doc in docList:
        dDoc = doc.to_dict()
        print("{} {:<14} {:<14} {:<14}".format(num, dDoc["name"], dDoc["location"], dDoc["time"]))
        num += 1


# add new order
def addOrder(db):
    print("Which customer is this order for?")
    printCustomers(db)
    print()
    name = input("> ")
    if (db.collection("customers").document(name).get().exists):
        print()
        print("What is the location of the order?")
        location = input("> ")
        print("What is the time of the order?")
        time = input("> ")
        db.collection("orders").document().set({"name" : name, "location" : location, "time" : time})
    else:
        print("Customer does not exist")


# changes value of field in an order
def editOrder(db):
    printOrders(db)
    print("What is the number of the order you want to edit?")
    docIdList = []
    orders = db.collection("orders").stream()
    for o in orders:
        #docIdList[number] += str(o.id)
        docIdList.append(o.id)
        #print(docIdList[number])

    #for doc in docIdList:
        #print(doc)
    num = int(input("> "))
    # print(docIdList[num - 1])
    while num <= 0 or num > len(docIdList):
        print("Number not valid")
        print("What is the number of the order you want to delete?")
        num = int(input("> "))
    order = db.collection("orders").document(docIdList[num - 1])
    while not order.get().exists:
        print("Order does not exist")
        print("What is the number of the order you want to edit?")
        num = input("> ")
        order = db.collection("orders").document(docIdList[num - 1])
    print("Which field would you like to edit?")
    print("Time (t)")
    print("Location (l)")
    print()
    which = ""
    again = True
    while again:
        which = ""
        which = input("> ")
        if which == "t":
            print("What is the new desired time?")
            nTime = input("> ")
            order.set({"time" : nTime}, merge=True)
            again = False
        elif which == "l":
            print("What is the new desired location?")
            nLocation = input("> ")
            order.set({"location" : nLocation}, merge=True)
            again = False
        else:
            print("Not a valid input")
 

# deletes order
def delOrder(db):
    printOrders(db)
    print("What is the number of the order you want to delete?")
    docIdList = []
    orders = db.collection("orders").stream()
    for o in orders:
        docIdList.append(o.id)

    num = int(input("> "))
    while num <= 0 or num > len(docIdList):
        print("Number not valid")
        print("What is the number of the order you want to delete?")
        num = int(input("> "))
    
    #print(docIdList[num - 1])
    
    order = db.collection("orders").document(docIdList[num - 1])
    while not order.get().exists:
        print("Order does not exist")
        print("What is the number of the order you want to delete?")
        order = db.collection("orders").document(docIdList[num - 1])


    print("Are you sure you want to delete this order? (y/n)")
    yon = input("> ")
    if yon == "y":
        order.delete()
    else:
        print("Order not deleted")



def main():
    db = initialize_firestore()

    quitFlag = False
    while not quitFlag:
        print()
        print("What would you like to do?")
        print()
        printOptions()
        print()
        answer = input("> ")
        # see customers
        if answer == "sc":
            printCustomers(db)
        # add customer
        elif answer == "ac":
            addCustomer(db)
        # edit customer
        elif answer == "ec":
            editCustomer(db)
        # delete customer
        elif answer == "dc":
            delCustomer(db)
        # see orders
        elif answer == "so":
            printOrders(db)
        # add order
        elif answer == "ao":
            addOrder(db)
        # edit order
        elif answer == "eo":
            editOrder(db) 
            pass
        # delete order
        elif answer == "do":
            delOrder(db)
            pass
        # clear
        elif answer == "c":
            clear()
        # quit
        elif answer == "q":
            quitFlag = True
        else:
            print("Not a valid option")

    print("Exiting...")


if __name__ == "__main__":
    main()