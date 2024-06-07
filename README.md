# Real-time Monitor Simulator

## Project Overview:
- This project implements a real-time medical monitoring system using Python, PyQt5 for the GUI, and Redis for the Database.
- Using the Socket Programming and TCP as the communication method between the client and the server
- The client is a GUI that handles both sending random data in the range of the specific vital Sign and visualize these data in a Line Graph or in a Table
- The server handles the request from the client side sent in a JSON format to standardize the request method and saves the data in redis database the key is the id, name, and the vital sign name joined together with a sperator as _ and the values is stored in the array linked to that specific key

## Components:
- Server: Manages incoming connections and data from the client, storing received medical data into Redis.
- GUI: Simulates patient data generation and sends this data to the server. Allows users to visualize the medical data in real-time, search for specific patients, and control the monitoring process.
- Redis: Used as a datastore to hold the medical data for all patients.


## Functionality:
- Add patient name and SSN as the ID for the patient
- Choose the type of vital signs to be monitored
- Search by ID functionality and able to plot different graphs related to the same patient on the same graph
- Filter by Vital Sign functionality in the table 
  
## Screen-Shots:
![Screenshot 2024-05-11 232207](https://github.com/MalakEltuny/app/assets/115397064/54c2b01d-dfb2-416f-b152-967ff8ca132b)


![Screenshot 2024-05-11 232219](https://github.com/MalakEltuny/app/assets/115397064/647f5501-2097-4c29-ac57-41b033ca5380)


![Screenshot 2024-05-11 232233](https://github.com/MalakEltuny/app/assets/115397064/1faf57f3-3e4c-4102-a4a2-a6035960b1a6)


![Screenshot 2024-05-11 232253](https://github.com/MalakEltuny/app/assets/115397064/df47b8c6-9b8a-4fd1-8559-1d2e4589f60b)


![Screenshot 2024-05-11 232306](https://github.com/MalakEltuny/app/assets/115397064/81e9db96-9f5a-4577-9be1-e31da7f1e46d)


![Screenshot 2024-05-11 232333](https://github.com/MalakEltuny/app/assets/115397064/ee77cded-5d40-4360-bd92-6650cfd86b89)


![Screenshot 2024-05-11 232349](https://github.com/MalakEltuny/app/assets/115397064/f25be40a-5663-4fa3-b86f-931957364bd3)


## Team Members:

| Name           | GitHub Username          |
|----------------|--------------------------|
| Youssef Afify       | [Youssef Afify](https://github.com/yusufafify)       |
| Malak Ahmed     | [Malak Ahmed](https://github.com/MalakEltuny)     |

