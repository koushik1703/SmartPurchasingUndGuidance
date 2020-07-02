from firebase import firebase
import datetime
import time

# Create the connection to our Firebase database - don't forget to change the URL!
FBConn = firebase.FirebaseApplication('https://spug-ca0fe.firebaseio.com/', None)


while True:
    
    # Ask the user to input a temperature
    temperature = int(input("What is the temperature? "))
    
    # Create a dictionary to store the data before sending to the database
    data_to_upload = {
        'Temp' : temperature
    }

    # Post the data to the appropriate folder/branch within your database
    result = FBConn.post('/SPUG_TestData/',data_to_upload)

    # Print the returned unique identifier
    print(result)
