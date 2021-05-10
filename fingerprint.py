from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QTime, QDateTime, Qt
from threading import Timer
from dotenv import load_dotenv
import threading
import time, json, requests, socket
import sys, os
import pygame

from pyfingerprint.pyfingerprint import PyFingerprint

# dotenv를 사용해 url주소 가져오기
load_dotenv(verbose=True)

URL_MAIN = os.getenv('URL_MAIN')
URL_NUMCHECK = os.getenv('URL_NUMCHECK')
URL_ENROLL = os.getenv('URL_ENROLL')
URL_DELETE = os.getenv('URL_DELETE')
URL_FINGER = os.getenv('URL_FINGER')
URL_LIMIT = os.getenv('URL_LIMIT')
URL_OUT = os.getenv('URL_OUT')

Main_ID ={
    "primaryKEY" : 'NULL',
    "tab" : 'true'
}

Main_CHECK = {
    "userName" : 'NULL',
    "data" : 'true',
    "check" : 'NULL'
}

Enroll_NAME = {
    "std_num" : ''
}

Enroll_FLAG = {
    "enroll_flag" : 'false',
    "flag_exist": 'false',  # 입력한 학번 존재 유무 확인 값
    "userName": 'NULL'
}

Enroll_ID = {
    "userID": 'NULL',       # 사용자 이름
    "primaryKEY": 'NULL',   # 사용자 지문 번호
}

Delete_ID = {
    "primaryKEY" : 'NULL'
}

Outgo_ID = {
    "primaryKEY" : 'NULL',
    "reason" : '식사'
}

Outgo_FLAG = {
        "std_name" : "null",
        "in_time" : "null",
        "out_time" : "null",
        "reason" : "null",
        "outgoing_time":"null"
    }

Std_DATA = {

}

pygame.mixer.init(16000, -16, 1, 2048)
alarm = pygame.mixer.music.load("/home/pi/Desktop/alarm.mp3")

# 지문인식기 연결
try:
    f = PyFingerprint('/dev/ttyAMA0', 57600, 0xFFFFFFFF, 0x00000000)
    ## BaudRate, ## address , ## password
except Exception as e:
    print('센서 정보를 확인할 수 없습니다!')
    exit(1)

def get_Finger_List():
    response = requests.post(URL_FINGER)
    finger_list = json.loads(response.text)
    f.clearDatabase()
    for i in range(0, len(finger_list)):
        #f.deleteTemplate(i)
        f.uploadCharacteristics(0x01, eval(finger_list[i]['serial_num']))
        f.createTemplate()
        positionNumber = f.storeTemplate()
        Std_DATA[i] = finger_list[i]['std_num']
time.sleep(5)

try:
    get_Finger_List()
except Exception as e:
    sys.stdout = open('error.txt','w')
    
def reset_all_dic():
    global Main_ID, Main_CHECK, Enroll_NAME, Enroll_FLAG, Enroll_ID, Delete_ID, Outgo_ID, Outgo_FLAG
    Main_ID ={
        "primaryKEY" : 'NULL',
        "tab" : 'true'
    }

    Main_CHECK = {
        "userName" : 'NULL',
        "data" : 'true',
        "check" : 'NULL'
    }

    Enroll_NAME = {
        "std_num" : ''
    }

    Enroll_FLAG = {
        "enroll_flag": 'false',
        "flag_exist": 'false',  # 입력한 학번 존재 유무 확인 값
        "userName": 'NULL'
    }

    Enroll_ID = {
        "userID": 'NULL',       # 사용자 이름
        "primaryKEY": 'NULL',   # 사용자 지문 번호
    }

    Delete_ID = {
        "primaryKEY" : 'NULL'
    }

    Outgo_ID = {
        "primaryKEY" : 'NULL'
    }

    Outgo_FLAG = {
        "std_name" : "",
        "in_time" : "",
        "out_time" : "",
        "reason" : "",
        "outgoing_time" : ""
    }


def search_finger_data(data, mode='finger'):
    if mode == 'finger':
        for i in range(0, len(data)):
            f.uploadCharacteristics(0x02,eval(data[i]['serial_num']))
            score = f.compareCharacteristics()
            if score != 0:
                Main_ID['primaryKEY'] = data[i]['std_num']
                return score
    else:
        for i in range(0, len(data)):
            f.uploadCharacteristics(0x02,eval(data[i]['serial_num']))
            score = f.compareCharacteristics()
            if score != 0:
                Delete_ID['primaryKEY'] = data[i]['std_num']
                return True
    f.storeTemplate(0x02)
    return 0

class Ui_Dialog(object):

    def __init__(self):
        super().__init__()
        self.enroll_flag = False
        self.first_flag = True
        #get_Finger_List()

    def setupUi(self, Dialog):
        # 지문인식기 메인 윈도우
        Dialog.setObjectName("FingerPrint")
        Dialog.resize(800, 480)

        # 메인 탭
        self.tabWidget = QtWidgets.QTabWidget(Dialog)
        self.tabWidget.setGeometry(QtCore.QRect(-4, -1, 811, 481))
        self.tabWidget.setObjectName("tabWidget")
        self.tabWidget.setStyleSheet("QTabBar::tab{width: 200px; height:50px;}")
        self.Main = QtWidgets.QWidget()
        self.Main.setObjectName("Main")

        # 메인 화면 시간 표시 텍스트
        self.label_time = QtWidgets.QLabel(self.Main)
        self.label_time.setGeometry(QtCore.QRect(70, 50, 651, 131))
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setPointSize(40)
        font.setBold(True)
        font.setWeight(75)
        font.setStrikeOut(False)
        self.label_time.setFont(font)
        self.label_time.setAutoFillBackground(True)
        self.label_time.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.label_time.setScaledContents(False)
        self.label_time.setAlignment(QtCore.Qt.AlignCenter)
        self.label_time.setObjectName("label_time")

        # 메인 화면 안내메세지 텍스트
        self.label_text = QtWidgets.QLabel(self.Main)
        self.label_text.setGeometry(QtCore.QRect(70, 270, 651, 131))
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)
        self.label_text.setFont(font)
        self.label_text.setAutoFillBackground(True)
        self.label_text.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.label_text.setFrameShadow(QtWidgets.QFrame.Plain)
        self.label_text.setAlignment(QtCore.Qt.AlignCenter)
        self.label_text.setObjectName("label_text")

        # 메인 화면 입/퇴실 라디오 버튼 그룹
        self.groupBox = QtWidgets.QGroupBox(self.Main)
        self.groupBox.setGeometry(QtCore.QRect(70, 200, 600, 51))
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.button_in = QtWidgets.QRadioButton(self.groupBox)
        self.button_in.setGeometry(QtCore.QRect(10, 10, 181, 41))
        self.button_in.setObjectName("button_in")
        self.button_out = QtWidgets.QRadioButton(self.groupBox)
        self.button_out.setGeometry(QtCore.QRect(350, 10, 181, 41))
        self.button_out.setObjectName("button_out")
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setPointSize(20)
        self.button_in.setFont(font)
        self.button_out.setFont(font)
        self.button_in.clicked.connect(self.change_state_in)
        self.button_out.clicked.connect(self.change_state_out)
        self.tabWidget.addTab(self.Main, "")
        
        # 지문 등록 탭
        self.Enroll = QtWidgets.QWidget()
        self.Enroll.setObjectName("Enroll")
        self.tabWidget.addTab(self.Enroll, "")

        # 지문 등록 넘버패드
        self.numpad0 = QtWidgets.QPushButton(self.Enroll)
        self.numpad0.setGeometry(QtCore.QRect(20, 190, 121, 111))
        self.numpad0.setObjectName("numpad0")
        self.numpad1 = QtWidgets.QPushButton(self.Enroll)
        self.numpad1.setGeometry(QtCore.QRect(150, 190, 121, 111))
        self.numpad1.setObjectName("numpad1")
        self.numpad2 = QtWidgets.QPushButton(self.Enroll)
        self.numpad2.setGeometry(QtCore.QRect(280, 190, 121, 111))
        self.numpad2.setObjectName("numpad2")
        self.numpad3 = QtWidgets.QPushButton(self.Enroll)
        self.numpad3.setGeometry(QtCore.QRect(410, 190, 121, 111))
        self.numpad3.setObjectName("numpad3")
        self.numpad4 = QtWidgets.QPushButton(self.Enroll)
        self.numpad4.setGeometry(QtCore.QRect(540, 190, 121, 111))
        self.numpad4.setObjectName("numpad4")
        self.numpad_back = QtWidgets.QPushButton(self.Enroll)
        self.numpad_back.setGeometry(QtCore.QRect(670, 190, 121, 111))
        self.numpad_back.setObjectName("numpad_back")
        self.numpad5 = QtWidgets.QPushButton(self.Enroll)
        self.numpad5.setGeometry(QtCore.QRect(20, 320, 121, 111))
        self.numpad5.setObjectName("numpad5")
        self.numpad6 = QtWidgets.QPushButton(self.Enroll)
        self.numpad6.setGeometry(QtCore.QRect(150, 320, 121, 111))
        self.numpad6.setObjectName("numpad6")
        self.numpad7 = QtWidgets.QPushButton(self.Enroll)
        self.numpad7.setGeometry(QtCore.QRect(280, 320, 121, 111))
        self.numpad7.setObjectName("numpad7")
        self.numpad8 = QtWidgets.QPushButton(self.Enroll)
        self.numpad8.setGeometry(QtCore.QRect(410, 320, 121, 111))
        self.numpad8.setObjectName("numpad8")
        self.numpad9 = QtWidgets.QPushButton(self.Enroll)
        self.numpad9.setGeometry(QtCore.QRect(540, 320, 121, 111))
        self.numpad9.setObjectName("numpad9")
        self.numpad_enter = QtWidgets.QPushButton(self.Enroll)
        self.numpad_enter.setGeometry(QtCore.QRect(670, 320, 121, 111))
        self.numpad_enter.setObjectName("numpad_enter")
        
        # 지문 등록 안내메세지 박스
        self.label_enroll = QtWidgets.QLabel(self.Enroll)
        self.label_enroll.setGeometry(QtCore.QRect(20, 30, 771, 131))
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)
        self.label_enroll.setFont(font)
        self.label_enroll.setAutoFillBackground(True)
        self.label_enroll.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.label_enroll.setScaledContents(False)
        self.label_enroll.setAlignment(QtCore.Qt.AlignCenter)
        self.label_enroll.setObjectName("label_enroll")
        
        # 넘버패드 클릭 시, 실행 될 함수 연결
        self.numpad0.clicked.connect(self.num_input0)
        self.numpad1.clicked.connect(self.num_input1)
        self.numpad2.clicked.connect(self.num_input2)
        self.numpad3.clicked.connect(self.num_input3)
        self.numpad4.clicked.connect(self.num_input4)
        self.numpad5.clicked.connect(self.num_input5)
        self.numpad6.clicked.connect(self.num_input6)
        self.numpad7.clicked.connect(self.num_input7)
        self.numpad8.clicked.connect(self.num_input8)
        self.numpad9.clicked.connect(self.num_input9)
        self.numpad_back.clicked.connect(self.num_back)
        self.numpad_enter.clicked.connect(self.enroll_send)

        # 지문 삭제 탭
        self.Delete = QtWidgets.QWidget()
        self.Delete.setObjectName("Delete")
        self.tabWidget.addTab(self.Delete, "")
        
        # 지문 삭제 안내메세지 텍스트
        self.label_delete = QtWidgets.QLabel(self.Delete)
        self.label_delete.setGeometry(QtCore.QRect(70, 130, 651, 131))
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setPointSize(32)
        font.setBold(True)
        font.setWeight(75)
        self.label_delete.setFont(font)
        self.label_delete.setAutoFillBackground(True)
        self.label_delete.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.label_delete.setFrameShadow(QtWidgets.QFrame.Plain)
        self.label_delete.setAlignment(QtCore.Qt.AlignCenter)
        self.label_delete.setObjectName("label_text")

        # 외출 탭
        self.Outgo = QtWidgets.QWidget()
        self.Outgo.setObjectName("Out")
        self.tabWidget.addTab(self.Outgo, "")

        # 외출 탭 시간 표시 텍스트
        self.out_time = QtWidgets.QLabel(self.Outgo)
        self.out_time.setGeometry(QtCore.QRect(70, 50, 651, 131))
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setPointSize(40)
        font.setBold(True)
        font.setWeight(75)
        font.setStrikeOut(False)
        self.out_time.setFont(font)
        self.out_time.setAutoFillBackground(True)
        self.out_time.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.out_time.setScaledContents(False)
        self.out_time.setAlignment(QtCore.Qt.AlignCenter)
        self.out_time.setObjectName("out_time")

        # 외출 탭 안내메세지 텍스트
        self.label_out = QtWidgets.QLabel(self.Outgo)
        self.label_out.setGeometry(QtCore.QRect(70, 270, 651, 131))
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)
        self.label_out.setFont(font)
        self.label_out.setAutoFillBackground(True)
        self.label_out.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.label_out.setFrameShadow(QtWidgets.QFrame.Plain)
        self.label_out.setAlignment(QtCore.Qt.AlignCenter)
        self.label_out.setObjectName("label_out")

        # 외출 사유 버튼
        self.out_groupBox = QtWidgets.QGroupBox(self.Outgo)
        self.out_groupBox.setGeometry(QtCore.QRect(70, 200, 700, 51))
        self.out_groupBox.setTitle("")
        self.out_groupBox.setObjectName("out_groupBox")
        self.button_meal = QtWidgets.QRadioButton(self.out_groupBox)
        self.button_meal.setGeometry(QtCore.QRect(25, 10, 181, 41))
        self.button_meal.setObjectName("button_meal")
        self.button_mensetsu = QtWidgets.QRadioButton(self.out_groupBox)
        self.button_mensetsu.setGeometry(QtCore.QRect(170, 10, 181, 41))
        self.button_mensetsu.setObjectName("button_mensetsu")
        self.button_gz = QtWidgets.QRadioButton(self.out_groupBox)
        self.button_gz.setGeometry(QtCore.QRect(355, 10, 181, 41))
        self.button_gz.setObjectName("button_gz")
        self.button_etc = QtWidgets.QRadioButton(self.out_groupBox)
        self.button_etc.setGeometry(QtCore.QRect(540, 10, 181, 41))
        self.button_etc.setObjectName("button_etc")
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setPointSize(20)
        self.button_meal.setFont(font)
        self.button_mensetsu.setFont(font)
        self.button_gz.setFont(font)
        self.button_etc.setFont(font)
        self.button_meal.clicked.connect(self.change_state_meal)
        self.button_mensetsu.clicked.connect(self.change_state_mensetsu)
        self.button_gz.clicked.connect(self.change_state_gz)
        self.button_etc.clicked.connect(self.change_state_etc)
        self.tabWidget.addTab(self.Outgo, "")

        # 스타일시트
        # 메인페이지
        self.label_time.setStyleSheet("color:#414c5d; background-color:#ffffff;\
        border:2px solid #414c5d")
        self.label_text.setStyleSheet("color:#414c5d; background-color:#FFFFFF;\
        border:2px solid #414c5d")
        self.groupBox.setStyleSheet("color:#414c5d")

        # 지문 등록
        self.label_enroll.setStyleSheet("color:#414c5d; background-color:#ffffff;\
        border:2px solid #414c5d")
        self.numpad0.setStyleSheet("color:#414c5d; background-color:#ffffff;\
        border:1px solid #414c5d")
        self.numpad1.setStyleSheet("color:#414c5d; background-color:#ffffff;\
        border:1px solid #414c5d")
        self.numpad2.setStyleSheet("color:#414c5d; background-color:#ffffff;\
        border:1px solid #414c5d")
        self.numpad3.setStyleSheet("color:#414c5d; background-color:#ffffff;\
        border:1px solid #414c5d")
        self.numpad4.setStyleSheet("color:#414c5d; background-color:#ffffff;\
        border:1px solid #414c5d")
        self.numpad5.setStyleSheet("color:#414c5d; background-color:#ffffff;\
        border:1px solid #414c5d")
        self.numpad6.setStyleSheet("color:#414c5d; background-color:#ffffff;\
        border:1px solid #414c5d")
        self.numpad7.setStyleSheet("color:#414c5d; background-color:#ffffff;\
        border:1px solid #414c5d")
        self.numpad8.setStyleSheet("color:#414c5d; background-color:#ffffff;\
        border:1px solid #414c5d")
        self.numpad9.setStyleSheet("color:#414c5d; background-color:#ffffff;\
        border:1px solid #414c5d")
        self.numpad_back.setStyleSheet("color:#414c5d; background-color:#ffffff;\
        border:1px solid #414c5d")
        self.numpad_enter.setStyleSheet("color:#414c5d; background-color:#ffffff;\
        border:1px solid #414c5d")

        # 지문 삭제
        self.label_delete.setStyleSheet("color:#414c5d; background-color:#ffffff;\
        border:2px solid #414c5d")

        # 외출
        self.out_time.setStyleSheet("color:#414c5d; background-color:#ffffff;\
        border:2px solid #414c5d")
        self.label_out.setStyleSheet("color:#414c5d; background-color:#ffffff;\
        border:2px solid #414c5d")
        self.out_groupBox.setStyleSheet("color:#414c5d")

        self.retranslateUi(Dialog)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):

        _translate = QtCore.QCoreApplication.translate

        Dialog.setWindowTitle(_translate("Dialog", "FingerPrint"))
        self.label_time.setText(_translate("Dialog", "시간"))
        self.label_text.setText(_translate("Dialog", "지문을 찍어주세요"))
        self.button_in.setText(_translate("Dialog", "출석"))
        self.button_in.setChecked(True)
        self.button_out.setText(_translate("Dialog", "퇴실"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Main), _translate("Dialog", "출석"))

        self.label_enroll.setText(_translate("Dialog", "학번을 입력해주세요"))
        self.numpad0.setText(_translate("Dialog", "0"))
        self.numpad1.setText(_translate("Dialog", "1"))
        self.numpad2.setText(_translate("Dialog", "2"))
        self.numpad3.setText(_translate("Dialog", "3"))
        self.numpad4.setText(_translate("Dialog", "4"))
        self.numpad_back.setText(_translate("Dialog", "정정"))
        self.numpad5.setText(_translate("Dialog", "5"))
        self.numpad6.setText(_translate("Dialog", "6"))
        self.numpad7.setText(_translate("Dialog", "7"))
        self.numpad8.setText(_translate("Dialog", "8"))
        self.numpad9.setText(_translate("Dialog", "9"))
        self.numpad_enter.setText(_translate("Dialog", "확인"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Enroll), _translate("Dialog", "등록"))
        
        self.label_delete.setText(_translate("Dialog", "삭제할 지문을 찍어주세요"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Delete), _translate("Dialog", "삭제"))

        self.label_out.setText(_translate("Dialog", "사유 선택 후, 지문을 찍어주세요"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Outgo), _translate("Dialog", "외출"))
        self.button_meal.setText(_translate("Dialog", "식사"))
        self.button_meal.setChecked(True)
        self.button_mensetsu.setText(_translate("Dialog", "면접연습"))
        self.button_gz.setText(_translate("Dialog", "글로벌존"))
        self.button_etc.setText(_translate("Dialog", "기타"))

        self.showtime()
        self.mainMessage()

    # 시간 관련 함수
    def showtime(self):
        # 현재 시간을 구한 뒤, Label에 출력하기 위해서 str형으로 변환
        # 현재 날짜 및 시간
        current_date = QDateTime.currentDateTime()
        current_date = current_date.toString('yyyy-MM-dd\thh:mm:ss')
        # 하교시간 알람등에 사용할 시간만 따로 구하기
        current_time = QTime.currentTime()
        current_time = current_time.toString()
            
        # 하교시간 알람
        if current_time == "22:30:00":
            pygame.mixer.music.play()
        # 하교시간 리미트
        if current_time == "22:30:00":
            response = requests.post(URL_LIMIT)
            print(response.status_code)
        
        self.label_time.setText(current_date)
        self.out_time.setText(current_date)
        
        
        if self.button_in.isChecked():
            Main_ID['tab'] = 'true'
        else:
            Main_ID['tab'] = 'false'
        
        # 타이머 설정  (1초마다, 콜백함수)
        timer = Timer(1, self.showtime)
        timer.start()
        
    # 입실/퇴실 버튼 선택 시, 현재 상태 값 변경
    def change_state_in(self):
        Main_ID["tab"] = "true"
    def change_state_out(self):
        Main_ID["tab"] = "false"
    def change_state_meal(self):
        Outgo_ID["reason"] = "식사"
    def change_state_mensetsu(self):
        Outgo_ID["reason"] = "면접연습"
    def change_state_gz(self):
        Outgo_ID["reason"] = "글로벌존"
    def change_state_etc(self):
        Outgo_ID["reason"] = "기타"
        #print(Outgo_ID)
        
    def select_reason(self):
        if self.button_meal.isChecked():
            Outgo_ID["reason"] = "식사"
        elif self.button_mensetsu.isChecked():
            Outgo_ID["reason"] = "면접연습"
        elif self.button_gz.isChecked():
            Outgo_ID["reason"] = "글로벌존"
        elif self.button_etc.isChecked():
            Outgo_ID["reason"] = "기타"
    
    # 입력한 넘버패드 버튼에 따라 서버에 전송할 학번 값 수정
    def num_input0(self):
        Enroll_NAME["std_num"] += "0"
        self.label_enroll.setText(Enroll_NAME["std_num"])
    def num_input1(self):
        Enroll_NAME["std_num"] += "1"
        self.label_enroll.setText(Enroll_NAME["std_num"])
    def num_input2(self):
        Enroll_NAME["std_num"] += "2"
        self.label_enroll.setText(Enroll_NAME["std_num"])
    def num_input3(self):
        Enroll_NAME["std_num"] += "3"
        self.label_enroll.setText(Enroll_NAME["std_num"])
    def num_input4(self):
        Enroll_NAME["std_num"] += "4"
        self.label_enroll.setText(Enroll_NAME["std_num"])
    def num_input5(self):
        Enroll_NAME["std_num"] += "5"
        self.label_enroll.setText(Enroll_NAME["std_num"])
    def num_input6(self):
        Enroll_NAME["std_num"] += "6"
        self.label_enroll.setText(Enroll_NAME["std_num"])
    def num_input7(self):
        Enroll_NAME["std_num"] += "7"
        self.label_enroll.setText(Enroll_NAME["std_num"])
    def num_input8(self):
        Enroll_NAME["std_num"] += "8"
        self.label_enroll.setText(Enroll_NAME["std_num"])
    def num_input9(self):
        Enroll_NAME["std_num"] += "9"
        self.label_enroll.setText(Enroll_NAME["std_num"])
    def num_back(self):
        Enroll_NAME["std_num"] = ""
        self.label_enroll.setText("학번을 입력해주세요")
    

    # 지문등록 확인 버튼 클릭 시, 실행할 함수
    def enroll_send(self):
        try:
            ## POST 통신을 이용하여 DB로 학번을 전송 후 존재 유무 수신
            response = requests.post(URL_NUMCHECK, data=Enroll_NAME)
            ## 돌아오는 존재 유무 값을 받은후 json 형에서 다시 딕셔너리로 변환
            Enroll_FLAG = json.loads(response.text)
        except Exception as e:
            self.label_enroll.setText("네트워크 에러 발생!!\n다시 진행해주세요")
            self.mainMessage()
            
        if(Enroll_FLAG["flag_serial"] == "false"):
            self.label_enroll.setText(Enroll_FLAG["userName"] + "님 지문 데이터가 존재합니다")
            reset_all_dic()
        elif(Enroll_FLAG["flag_exist"] == "true"):
            self.enroll_flag = True
            self.label_enroll.setText(Enroll_FLAG["userName"] + "님 지문 등록을 진행합니다\n센서에 손가락을 올려주세요")
        else:
            self.label_enroll.setText("등록정보가 확인되지 않습니다")
            reset_all_dic()
        
    def mainMessage(self):
        reset_all_dic()
        
        if self.first_flag:
            self.first_flag = False
        else:
            while f.readImage() == False:
                pass

            f.convertImage(0x01)
                
            result = f.searchTemplate()
            
            positionNumber = result[0]
            score = result[1]
            
            
            ## 메인 출석화면
            if self.tabWidget.currentIndex() == 0:
                self.label_enroll.setText("학번을 입력해주세요")
                self.label_delete.setText("삭제할 지문을 찍어주세요")
                self.label_out.setText("사유 선택 후, 지문을 찍어주세요")

                ## 지문 검사
                if positionNumber == -1: 
                    self.label_text.setText("등록되지 않은 지문입니다")
                    time.sleep(1)
                else:
                    if score >= 55:
                        try:
                            Main_ID['primaryKEY'] = Std_DATA[positionNumber]
                            response = requests.post(URL_MAIN, data=Main_ID)
                            Main_CHECK = json.loads(response.text)
                        except Exception as e:
                            sys.stdout = open('error.txt','w')
                            error_date = QDateTime.currentDateTime()
                            error_date = error_date.toString('yyyy-MM-dd hh:mm:ss')
                            print(error_date," : ",e,"\n")
                            self.label_text.setText("네트워크 에러 발생!!\n다시 진행해주세요")
                            self.mainMessage()
                        
                        ## True => 정상처리, False => 정상처리x
                        if Main_CHECK['data']:
                            if Main_ID['tab'] == 'true':
                                self.label_text.setText(Main_CHECK['userName']+"님 입실처리 되었습니다")
                            else:
                                self.label_text.setText(Main_CHECK['userName']+"님 퇴실처리 되었습니다")
                        else:
                            self.label_text.setText("입/퇴실 버튼을 확인하세요")
                    else:
                        self.label_text.setText("인식률이 낮습니다. 다시 인증해주세요")
            ## 지문 등록            
            elif self.tabWidget.currentIndex() == 1:

                self.label_text.setText("지문을 찍어주세요")
                self.label_delete.setText("삭제할 지문을 찍어주세요")
                self.label_out.setText("사유 선택 후, 지문을 찍어주세요")
                
                # 지문 등록 진행이 가능한 경우
                if self.enroll_flag:
                    # 이미 등록된 지문인 경우
                    if positionNumber != -1:
                        self.label_enroll.setText("이미 등록된 지문입니다")
                    else:
                        self.label_enroll.setText("센서에 다시 손가락을 올려주세요")
                        
                        ## 다시 손가락을 올릴 때 까지 대기
                        while f.readImage() == False:
                            pass

                        ## 읽은 이미지를 문자열로 변환
                        f.convertImage(0x02)
                        
                        if positionNumber != -1:
                            self.label_enroll.setText("이미 등록된 지문입니다")
                        else:
                            ## 지문정보를 비교, 정확도가 낮은 경우
                            if f.compareCharacteristics() == 0:
                                self.label_enroll.setText("정확도가 낮습니다\n조금 더 정확하게 찍어주세요")
                                
                            ## 등록된 지문이 아니고, 정확도가 높은 경우
                            else:
                                try:
                                    Enroll_ID["primaryKEY"] = str(f.downloadCharacteristics(0x01)).encode('utf-8')
                                    Enroll_ID["userID"] = Enroll_NAME["std_num"]
                                    response = requests.post(URL_ENROLL, data=Enroll_ID)
                                    Enroll_FLAG = json.loads(response.text)
                                except Exception as e:
                                    sys.stdout = open('error.txt','w')
                                    error_date = QDateTime.currentDateTime()
                                    error_date = error_date.toString('yyyy-MM-dd hh:mm:ss')
                                    print(error_date," : ",e,"\n")
                                    self.label_enroll.setText("네트워크 에러 발생!!\n다시 진행해주세요")
                                    self.mainMessage()
                                
                                f.createTemplate()
                                positionNumber = f.storeTemplate()
                                Std_DATA[positionNumber] = Enroll_NAME['std_num']
                                
                                self.label_enroll.setText(Enroll_FLAG['userName']+"님 지문등록 성공!!")
                else:
                    self.label_enroll.setText("학번을 먼저 입력해 주세요")
                self.enroll_flag = False
            ## 지문 삭제
            elif self.tabWidget.currentIndex() == 2:
                self.label_text.setText("지문을 찍어주세요")
                self.label_enroll.setText("학번을 입력해주세요")
                self.label_out.setText("사유 선택 후, 지문을 찍어주세요")

                ## 지문 넘버에 따른 진행과정
                if positionNumber != -1:
                    try:
                        Delete_ID['primaryKEY'] = Std_DATA[positionNumber]
                        response = requests.post(URL_DELETE, data=Delete_ID)
                        f.deleteTemplate(positionNumber)
                    except Exception as e:
                        sys.stdout = open('error.txt','w')
                        error_date = QDateTime.currentDateTime()
                        error_date = error_date.toString('yyyy-MM-dd hh:mm:ss')
                        print(error_date," : ",e,"\n")
                        self.label_delete.setText("네트워크 에러 발생!!\n다시 진행해주세요")
                        self.mainMessage()
                        
                    self.label_delete.setText("지문이 삭제되었습니다")
                else:
                    self.label_delete.setText("지문정보가 잘못되었습니다")
            ## 외출
            elif self.tabWidget.currentIndex() == 3:
                
                self.label_text.setText("지문을 찍어주세요")
                self.label_enroll.setText("학번을 입력해주세요")
                self.label_delete.setText("삭제할 지문을 찍어주세요")

                if positionNumber != -1:
                    try:
                        self.select_reason()
                        Outgo_ID['primaryKEY'] = Std_DATA[positionNumber]
                        response = requests.post(URL_OUT, data=Outgo_ID)
                        Outgo_FLAG = json.loads(response.text)
                    except Exception as e:
                        sys.stdout = open('error.txt','w')
                        error_date = QDateTime.currentDateTime()
                        error_date = error_date.toString('yyyy-MM-dd hh:mm:ss')
                        print(error_date," : ",e,"\n")
                        self.label_out.setText("네트워크 에러 발생!!\n다시 진행해주세요")
                        self.mainMessage()
                        
                    if Outgo_FLAG['out_time'] == '00:00:00':
                        self.label_out.setText(Outgo_FLAG['std_name'] + "님 외출처리 되었습니다!\n사유 : " + Outgo_FLAG['reason'])
                    else:
                        self.label_out.setText(Outgo_FLAG['std_name'] + "님 복귀처리 되었습니다!\n외출시간 : " + Outgo_FLAG['outgoing_time'])
                else:
                    self.label_out.setText("지문정보가 잘못되었습니다")

        timer = Timer(1, self.mainMessage)
        timer.start()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.showFullScreen()
    sys.exit(app.exec_())
