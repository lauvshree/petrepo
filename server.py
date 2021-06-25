from flask import Flask, render_template, request, Response
import os, json, sys
from cloudant.client import Cloudant
from cloudant.error import CloudantException
from cloudant.result import Result, ResultByKey
from cloudant.document import Document
from dotenv import load_dotenv

load_dotenv()

databaseName = os.environ["databaseName"]
account_user_name = os.environ["account_user_name"]
apikey = os.environ["apikey"]


#Connect to the database
client = Cloudant.iam(account_name=account_user_name, api_key=apikey, connect=True)
myDatabase = client.create_database(databaseName)

app = Flask("Web Hook")

def getAllPets(kind):
    if(kind == "dog"):
        selector = {'kind': {'$eq': 'Dog'}}
        docs = myDatabase.get_query_result(selector)
        pets = []
        for doc in docs:
            pet_instance ={}
            pet_instance["id"] = doc["_id"]
            pet_instance["name"] = doc["name"]
            pet_instance["age"] = doc["age"]
            pet_instance["breed"] = doc["breed"]
            pets.append(pet_instance)
        return {"pets": pets}
    elif(kind == "cat"):
        selector = {'kind': {'$eq': 'Cat'}}
        docs = myDatabase.get_query_result(selector)
        for doc in docs:
            pet_instance ={}
            pet_instance["id"] = doc["id"]
            pet_instance["name"] = doc["name"]
            pet_instance["age"] = doc["age"]
            pet_instance["breed"] = doc["breed"]
            pets.append(pet_instance)
        return {"pets": pets}
    else:
        return {"pets":[]}

def getPetDetails(id):
    selector = {'_id': {'$eq': id}}
    docs = myDatabase.get_query_result(selector)
    for doc in docs:
        print("come here")
        pet_instance ={}
        pet_instance["name"] = doc["name"]
        pet_instance["age"] = doc["age"]
        pet_instance["breed"] = doc["breed"]
        pet_instance["comments"] = doc["comments"]
        return pet_instance

def getPetPic(id):
    selector = {'_id': {'$eq': id}}
    docs = myDatabase.get_query_result(selector)
    print(docs)
    for doc in docs:
        document = Document(myDatabase, document_id=id)
        attachment = document.get_attachment(attachment=doc['filename'],headers={"Content-Type":"jpeg/png"})
        return Response(attachment, mimetype='image/jpg')

    
@app.route("/pets",methods=["POST"])
def pets():
    pets = []

    if(request.args['req'] == "getAllPets"):
        return getAllPets(request.args['kind'])
    elif(request.args['req'] == "getPetDetails"):
        return getPetDetails(request.args['id'])
    elif(request.args['req'] == "getPetImage"):
        return getPetPic(request.args['id'])
    return {}

@app.route("/pet/<id>")
def petImage(id):
    return getPetPic(id)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
