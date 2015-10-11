from __init__ import app, db
from flask import Flask, request, redirect
from twilio.rest import TwilioRestClient
import twilio.twiml
from db_layer import Update, User


account = "" #ADD ACCOUNT
token = "" #ADD TOKEN
sender = "" #ADD SENDER
client = TwilioRestClient(account, token)

@app.route("/ChangePhoneNumber", methods=['GET','POST'])
def change_of_phone():

    phone = request.values.get('From', None)
    body = request.values.get('Body', None)
    model = db.findByField("phone_number", phone, Update)
    if model:
        user = db.findByField("username", model.username, User)  # the body is probably a password
        # user.password_hash now we need to compare user password hash to the password they gave us
    else:
        user = db.findByField("phone_number", phone, User)
        db.insert(Update(phone_number=phone, username=user.username))

    response = twilio.twiml.Response()

    '''
    NEED TO CONSIDER DIFFERENT LANGUAGE RESPONSE
    '''
    
    #If Phone Number is not in the table but the username is registered
        #response.message("Enter Password")
        #return str(response)
    #Else if Phone number is associated with username and password is correct
        #response.message("Profile Successfully Changed")
        #return str(response)

def create_message(reciever, sender, message):
    send_message = client.messages.create(to=reciever, from_=sender, body=message)

def send_message(user, post_array):
    message = None
    for post in post_array:
        if post["lang"] == user["preferred_language"]:
            message = post["body"]
            create_message(user["username"], sender, message)
    if not message:
        print "ERROR, CAN'T FIND SPECIFIED LANGUAGE"
