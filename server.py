from flask import Flask, render_template, request,Response, send_file
import json
import sys
from cloudant.client import Cloudant
from cloudant.error import CloudantException
from cloudant.result import Result, ResultByKey
from cloudant.document import Document

app = Flask("Web Hook")

@app.route("/pets", methods=["POST", "GET"])
def pet_pic():
    req = request.args["req"]
    if (req == "getAllPets"):
        return {"response":[{
                    "id": "1",
                    "name": "Hershey",
                    "age": "2 months",
                    "breed": "Cockerspaniel",
                    "Gender":"Female",
                    "comments": "Good dog"
                },
                {
                    "id": "2",
                    "name": "Romi",
                    "age": "10 months", 
                    "breed": "Pomeranian",
                    "Gender": "Female",
                    "comments": "Good dog"
                }]}
    elif (req == "getPetDetails"):
        pet_id = request.args["pet_id"]
        return send_file('static/dog.jpg', mimetype='image/jpg')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
