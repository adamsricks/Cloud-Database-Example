import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os
from os import system, name
import glob
import json



def initialize_firestore():
    """
    Create database connection
    """

    # Use the application default credentials
    cred = credentials.Certificate("private key.json")
    firebase_admin.initialize_app(cred)

    # Get reference to database
    db = firestore.client()
    return db

def clear():
    # for windows 
    if name == 'nt': 
        _ = system('cls') 
  
    # for mac and linux(here, os.name is 'posix') 
    else: 
        _ = system('clear') 

def addCustomer(db, first_name, last_name, location, phone):
    pass

def deleteCustomer(db, first_name, last_name):
    pass

def editCustomer(db, first_name, last_name):
    pass

def addOrder(db, first_name, last_name, location, time, order_contents):
    pass

def deleteOrder(db, order_id):
    pass

def editOrder(db, order_id):
    pass

# prints options
def printOptions():
    print("See all customers (sc)")
    print("Add customer (ac)")
    print("Delete customer (dc)")
    print("Edit customer (ec)")
    print("See all orders (so)")
    print("Add order (ao)")
    print("Delete order (do)")
    print("Edit order (eo)")
    print()
    print("Clear screen (c)")
    print("Exit (q)")

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
    print()

def collectionNameEnter():
    print("Which collection would you like to enter? (0,1,2,3,4) ")
    collection = input("> ")
    collection = returnCollection(collection)
    if collection == None:
        print("Please enter 0,1,2,3,4")
        collection = collectionNameEnter()
    else:
        return collection

def newDoc(db, collection):
    print("What is the name of your new doc?")
    name = input("> ")
    db.collection(collection).document(name).set({"name" : name})

def editDoc(db, collection):
    print("Which document would you like to edit?")
    name = input("> ")
    if (db.collection(collection).document(name).get().exists):
        return name
    else:
        print("Document does not exist")
        return None

def delDoc(db, collection):
    print("Which document would you like to delete?")
    document = input("> ") 
    print("Are you sure you want to delete this document? (y/n)")
    yon = input("> ")
    if yon == "y":
        if (db.collection(collection).document(document).get().exists):
            db.collection(collection).document(document).delete()
        else:
            print("Document does not exist")
    else:
        print("Document not deleted")

# changes value of document
def editField(db, collection, document):
    pass

# create a new field in a document
def newField(db, collection, document):
    pass

def delField(db, collection, document):
    print("Which field would you like to delete?")
    field = input("> ")    
    print("Are you sure you want to delete this field? (y/n)")
    yon = input("> ")
    if yon == "y":
        db.collection(collection).document(document).update({field: firestore.DELETE_FIELD })
    else:
        print("Field not deleted")



def main():
    db = initialize_firestore()

    quitFlag = False
    level = "r"
    collection = ""
    document = ""
    while not quitFlag:
        print()
        print("What would you like to do?")
        print()
        printOptions(level)
        print()
        answer = input("> ")
        # root level
        if level == "r":
            collection = ""
            # see all
            if answer == "s":
                printCollections()
            # enter collection
            elif answer == "e":
                level = "c"
                collection = collectionNameEnter()
            # quit
            elif answer == "q":
                quitFlag = True
            # clear screen
            elif answer == "c":
                clear()
            else:
                pass
        # collection level
        elif level == "c":
            # show all
            if answer == "s":
                printDocuments(db, collection)
            # exit collection
            elif answer == "ex":
                level = "r"
                collection = ""
            # edit document
            elif answer == "d":
                document = editDoc(db, collection)
                if document != None:
                    level = "d"
            # create new document
            elif answer == "n":
                newDoc(db, collection)
            # delete document
            elif answer == "x":
                delDoc(db, collection)
            # quit
            elif answer == "q":
                quitFlag = True
            # clear screen
            elif answer == "c":
                clear()
            else:
                pass
        # document level
        elif level == "d":
            # show all
            if answer == "s":
                printFields(db, collection, document)
            # exit document
            elif answer == "ex":
                level = "c"
                document = ""
            # quit
            elif answer == "d":
                pass
            elif answer == "n":
                pass
            elif answer == "x":
                pass
            elif answer == "q":
                quitFlag = True
            # clear screen
            elif answer == "c":
                clear()
            else:
                pass


    print("exiting...")


if __name__ == "__main__":
    main()