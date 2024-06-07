import socket
import random
import json
import time
import threading
import redis
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QTableWidgetItem
from pyqtgraph import mkPen
from random import randrange





client_socket = None
redis_client = redis.Redis(host='localhost', port=6379, db=0) #3ashan a connect el gui bel db 

patientId=""
patientName=""
vitalSign=""
vitalSignValues=[]


def startConnection(vitalNumber): 
    global client_socket
    # Check if the client socket is already open
    if client_socket and client_socket.fileno() != -1:
        print("Connection is already open. Closing it.")
        client_socket.close()
    
    # Initialize the client socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = 'localhost'  # or '127.0.0.1' to connect to the local machine
    port = 12345

    try:
        # Connect to the server
        client_socket.connect((host, port))

        # Receive initial message from the server
        message = client_socket.recv(1024)
        print(message.decode('ascii'))

        # Function to receive JSON response from the server
        def receive_json_response(client_socket): #el json hy-receive mn el server a binary messsage and converts it into a string 
            # Receive JSON data from the server
            json_data = client_socket.recv(1024).decode('ascii')
            
            # Decode JSON data
            try:
                response = json.loads(json_data)
                return response
            except json.JSONDecodeError:
                print("Received invalid JSON data from the server:", json_data)
                return None

        # Send JSON data to the server and receive JSON responses
        while True: #hena el json ba3t lel server a string message fa han7awelha le python dictionary 3ashan el server ye3raf ye2raha 
            # Prepare JSON data to send to the server
            if not client_socket:
                break
            data = {
                "id": int(patientId),
                "name": patientName,
                "vital_sign": vitalSign,
                "value": generateRandomVitalSign(vitalSign)
            }

            
            vitalNumber.display(int(data["value"])) #hena akhad el readings w bey-display them on the LCD 

            # Convert data to JSON format
            json_data = json.dumps(data)  

            # Send JSON data to the server
            client_socket.send(json_data.encode('ascii'))
            
            # Receive JSON response from the server
            response = receive_json_response(client_socket) 
            if response:
                print("Received JSON response from the server:")
                print("ID:", response["id"])
                print("Name:", response["name"])
                print("Vital Sign:", response["vitalSign"])
                print("Values:", response["values"])
            
            # Wait for 1 second before sending the next data
            time.sleep(1)
    except Exception as e:
        print("Error:", e)
        if client_socket:
          client_socket.close()


def handleSendBtn(self,vitalNumber): 
    global client_socket
    print("Testing connection...")
    if client_socket and client_socket.fileno() != -1:
        print("Closing the connection.")
        client_socket.close()
        print("Connection closed.")
        client_socket = None  # Reset the client_socket variable
        self.sendBtn.setText("Send")
    else:
        self.sendBtn.setText("Stop")
        print("Connection is open.")
        #get all keys from the database
        allKeys=redis_client.keys("*")
        # check if the id is the same but different name
        for key in allKeys:
            keyStr=key.decode('utf-8')
            if patientId==keyStr.split('_')[0] and patientName!=keyStr.split('_')[1]:
                QMessageBox.warning(None, "Alert", "Patient with the same Id already exists")
                return
        threading.Thread(target=startConnection, args=(vitalNumber,)).start()


def generateRandomVitalSign(vitalName):
    if vitalName == "respiratory":
        # Normal range for respiratory rate: between 12 and 20 breaths per minute
        return random.randint(12, 20)
      
    elif vitalName == "heart":
        # Normal range for heart rate: between 60 and 100 beats per minute
        return random.randint(60, 100)
        
    elif vitalName == "temperature":
        # Normal range for body temperature: between 36.1 and 37.2 degrees Celsius
        return round(random.uniform(36.1, 37.2), 1)
    else:
        print("Invalid vital sign name")

def handleRadioBtn(self,vitalName):
    global vitalSign
    vitalSign=vitalName

def handleTextChanged(self, text,boxType):
    global patientName
    global patientId
    if boxType=="name":
        patientName=text
    else:
        patientId=text


def handleSearchByIdButton(ID, name, vs,vitalGraph):
  global vitalSignValues
  vitalGraph.clear()
  redis_name = redis_client.keys(f'{ID}_*')
  print(redis_name)

  if not redis_name:
    QMessageBox.warning(None, "Alert", "Patient not found")
    name.setText("")  
    vs.setText("")
    return  
  if len(redis_name) > 1:
      vitalNameArray=[redis_name[i].decode("utf-8").split("_")[2] for i in range(len(redis_name))]
      print(vitalNameArray)
      ## put all the vitalNames in the vs.setText
      vs.setText(f'{vitalNameArray}')
      for i in range(len(redis_name)):
          values=[float(value) for value in redis_client.lrange(redis_name[i], 0, -1)]
          print(values)
          color = (randrange(256), randrange(256), randrange(256))

    # Create a pen with the random color
          pen = mkPen(color=color)
          vitalGraph.addLegend()
          vitalGraph.plot(values, name=f'{ID}_{redis_name[i].decode("utf-8").split("_")[1]}_{redis_name[i].decode("utf-8").split("_")[2]}',pen=pen)
          vitalGraph.show()
      name.setText(f'{redis_name[0].decode("utf-8").split("_")[1]}')
  else:
  
    redis_name_str = redis_name[0].decode('utf-8')
    print(redis_name_str.split("_"))
    name.setText(redis_name_str.split("_")[1])  
    vs.setText(redis_name_str.split("_")[2])
    values=redis_client.lrange(redis_name_str, 0, -1)
    vitalSignValues=[float(value) for value in values]
    color = (randrange(256), randrange(256), randrange(256))
    pen = mkPen(color=color)
    vitalGraph.addLegend()
    vitalGraph.plot(vitalSignValues,name=f'{ID}_{redis_name[0].decode("utf-8").split("_")[1]}_{redis_name[0].decode("utf-8").split("_")[2]}',pen=pen)
    vitalGraph.show()




    


def searchByVitalBtnClicked(self,searchByVitalTextBox, tableWidget):
    tableWidget.setRowCount(0)
    global redis_client
    
  
    # Search for relevant data in the Redis database
    if(searchByVitalTextBox==""):
        keys = redis_client.keys(f'*')
    else:
        keys = redis_client.keys(f'*_{searchByVitalTextBox}*')
  
    for key in keys:
        key_str = key.decode('utf-8')
        patient_id = key_str.split("_")[0]
        name = key_str.split("_")[1]
        vital_sign = key_str.split("_")[2]
        values = redis_client.lrange(key, 0, -1)
        values = [float(value) for value in values]
      
        row_position = tableWidget.rowCount()
        tableWidget.insertRow(row_position)
        tableWidget.setItem(row_position, 0, QTableWidgetItem(patient_id))
        tableWidget.setItem(row_position, 1, QTableWidgetItem(name))
        tableWidget.setItem(row_position, 2, QTableWidgetItem(vital_sign))
        tableWidget.setItem(row_position, 3, QTableWidgetItem(str(values)))
    tableWidget.sortItems(0)

def getAllData(self,tableWidget):
    
    global redis_client
    tableWidget.setRowCount(0)

  
    # Search for relevant data in the Redis database
    keys = redis_client.keys("*")
  
    for key in keys:
        key_str = key.decode('utf-8')
        patient_id = key_str.split("_")[0]
        name = key_str.split("_")[1]
        vital_sign = key_str.split("_")[2]
        values = redis_client.lrange(key, 0, -1)
        values = [float(value) for value in values]
      
        row_position = tableWidget.rowCount()
        tableWidget.insertRow(row_position)
        tableWidget.setItem(row_position, 0, QTableWidgetItem((patient_id)))
        tableWidget.setItem(row_position, 1, QTableWidgetItem(name))
        tableWidget.setItem(row_position, 2, QTableWidgetItem(vital_sign))
        tableWidget.setItem(row_position, 3, QTableWidgetItem(str(values)))
    tableWidget.sortItems(0)