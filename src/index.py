import json
import requests
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

def hello(event, context):
    # Initialize the Firestore app with the service account key
    cred = credentials.Certificate('./firebase.json')  # Replace with the path to your service account key file
    firebase_admin.initialize_app(cred)

    # Get a reference to the Firestore database
    db = firestore.client()

    # Create a new document in a collection
    collection_ref = db.collection('dogs')  # Replace 'your-collection' with the actual collection name

    # Fetch data from the API
    url = 'https://api.thedogapi.com/v1/breeds'  # Replace with the URL of the API
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        api_data = response.json()  # Use a different variable name here
        for i in range(0, 5):
            print(str(i) + "th dogs------")
            print(api_data[i].get('name', ''))
            print(api_data[i].get('bred_for', ''))
            print(api_data[i].get('temperament', ''))
            # Data to be added
            data = {
                'name': api_data[i].get('name', ''),
                'bred_for': api_data[i].get('bred_for', ''),
                'temperament': api_data[i].get('temperament', '')
            }
            # Add the data to Firestore
            doc_ref = collection_ref.add(data)
            print('Document written with ID:', doc_ref[1].id)
    else:
        print('Error occurred while fetching data:', response.status_code)   

    body = {
        "message": "Python AWS Lambda"
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response
