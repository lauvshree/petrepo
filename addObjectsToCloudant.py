#!/usr/bin/env python

# Connect to service instance by running import statements.
from cloudant.client import Cloudant
from cloudant.error import CloudantException
from cloudant.result import Result, ResultByKey
from cloudant.document import Document
import os, json

from dotenv import load_dotenv


load_dotenv()

account_user_name = os.environ["account_user_name"]
apikey = os.environ["apikey"]
databaseName = os.environ["pets-database"]


def main():
    client = Cloudant.iam(account_name=account_user_name, api_key=apikey, connect=True)
    myDatabaseDemo = client.create_database(databaseName)
    f = open('sample_pets.json',)
    data = json.load(f)
    for document in data["pets"]:
        kind = document["kind"]
        name = document['name']
        age = document['age']
        breed = document['breed']
        comments = document['comments']
        filename = document['filename']

        jsonDocument = {
                "kind": kind,
                "name": name,
                "age": age,
                "breed": breed,
                "comments": comments,
                "filename": filename
            }

         # Create a document by using the Database API.
        newDocument = myDatabaseDemo.create_document(jsonDocument)
        path = "pet_pics/"+document['filename']
        with open(path, 'rb') as f:
            contents = f.read()
        newDocument.put_attachment(filename, "image/jpg", contents, headers={})

if __name__=='__main__':
    main()

