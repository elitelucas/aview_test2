import json
import requests
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

def hello(event, context):
    # Initialize the Firestore app with the service account key
    cred = credentials.Certificate('./firebase.json')
    firebase_admin.initialize_app(cred)

    # Get a reference to the Firestore database
    db = firestore.client()

    # Create a new document in a collection
    collection_ref = db.collection('dogs')  

    # Fetch data from the API
    url = 'https://api.thedogapi.com/v1/breeds'  # Replace with the URL of the API
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        api_data = response.json()  # Use a different variable name here
        for i in range(0, 5):
            print("------#" + str(i+1) + " dog------")
            print(api_data[i].get('name', ''))
            # Data to be added
            data = {
                'name': api_data[i].get('name', ''),
                'bred_for': api_data[i].get('bred_for', ''),
                'temperament': api_data[i].get('temperament', '')
            }
            # Add the data to Firestore
            doc_ref = collection_ref.add(data)
            print('Document written with ID:', doc_ref[1].id)
        
        message = "success"
    else:
        print('Error occurred while fetching data:', response.status_code)   
        message = "error"

    response = {
        "statusCode": 200,
        "body": json.dumps({
            "message": message
        })
    }

    return response
