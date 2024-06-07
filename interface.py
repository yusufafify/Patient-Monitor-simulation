from PyQt5 import QtWidgets
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QPushButton,QRadioButton,QTextEdit,QLCDNumber
import functions
import pyqtgraph

def initConnectors(self):
    
    # Vital Sign Value LCD
    vitalNumber=self.findChild(QLCDNumber,"lcdNumber")

    #Send Btn connection
    self.sendBtn=self.findChild(QPushButton,"send_button")
    self.sendBtn.clicked.connect(lambda: functions.handleSendBtn(self,vitalNumber))

    #Vital Sign  Radio btn
    bodyTemp=self.findChild(QRadioButton,"bodytemp_radioButton")
    respiratoryRadio=self.findChild(QRadioButton,"respiratory_radioButton")
    heartRate=self.findChild(QRadioButton,"heartrate_radioButton")

    bodyTemp.clicked.connect(lambda: functions.handleRadioBtn(self,"temperature"))
    respiratoryRadio.clicked.connect(lambda: functions.handleRadioBtn(self,"respiratory"))
    heartRate.clicked.connect(lambda: functions.handleRadioBtn(self,"heart"))

    # Name and ID connection
    patientName=self.findChild(QTextEdit,"name_textbox")
    patientName.textChanged.connect(lambda: functions.handleTextChanged(self,patientName.toPlainText(),'name'))

    patientId=self.findChild(QTextEdit,"id_textbox")
    patientId.textChanged.connect(lambda: functions.handleTextChanged(self,patientId.toPlainText(),'id'))


    # Search by ID button functionality
    searchIdBTN= self.findChild(QPushButton, "search_button")
    searchIdBTN.clicked.connect(lambda: functions.handleSearchByIdButton(searchByIdTXB.toPlainText(), ByName, VtSignTBX,vitalGraph))

    searchByIdTXB= self.findChild(QTextEdit,"searchbyid_textbox")

    #searchByIdTXB.textChanged.connect(lambda: functions.handleSearchById(searchByIdTXB.toPlainText()))

    # byName Textbox functionality
    ByName=self.findChild(QTextEdit, "displayed_name_textbox") 
    ByName.setReadOnly(True)
    

    #Type of vital signs functionality 
    VtSignTBX= self.findChild(QTextEdit, "displayed_vital_sign_textbox")
    VtSignTBX.setReadOnly(True)

    
    #Vital Graph
    vitalGraph=self.findChild(pyqtgraph.PlotWidget, "widget")

    #Table Widget
    tableWidget=self.findChild(QtWidgets.QTableWidget,"tableWidget")

    # search by vitalSign textbox
    searchByVitalSignTXB=self.findChild(QTextEdit,"searchByVitalTextBox")
    # search by vital sign in table
    searchByVitalSignBTN=self.findChild(QPushButton,"searchByVitalBtn")
    searchByVitalSignBTN.clicked.connect(lambda: functions.searchByVitalBtnClicked(self,searchByVitalSignTXB.toPlainText(),tableWidget))

    #tab widget
    tableTab=self.findChild(QtWidgets.QTabWidget,"tableTab")
    tableTab.currentChanged.connect(lambda: functions.getAllData(self,tableWidget))

    
    

  

