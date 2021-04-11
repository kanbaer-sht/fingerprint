from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QMessageBox
from threading import Timer
import threading
import time, json, requests
import sys
import pygame

from pyfingerprint.pyfingerprint import PyFingerprint

Main_ID ={
    "primaryKEY" : 'NULL',
    "tabNum" : 'NULL',
    "tab" : 'true'
}

Main_CHECK = {
    "userName" : 'NULL',
    "data" : 'true',
    "check" : 'NULL'
}

Enroll_NAME = {
    "std_num" : '',
    "tabNum" : 'NULL'       # 현재 탭 넘버링
}

Enroll_FLAG = {
    "flag_exist": 'false',  # 입력한 학번 존재 유무 확인 값
    "userName": 'NULL'
}

Enroll_ID = {
    "userID": 'NULL',       # 사용자 이름
    "primaryKEY": 'NULL',   # 사용자 지문 번호
}

Delete_ID = {
    "primaryKEY" : 'null'
}

pygame.mixer.init(16000, -16, 1, 2048)
alarm = pygame.mixer.music.load("/home/pi/Desktop/alarm.mp3")

try:
    f = PyFingerprint('/dev/ttyAMA0', 57600, 0xFFFFFFFF, 0x00000000)
    ## BaudRate, ## address , ## password
except Exception as e:
    print('센서 정보를 확인할 수 없습니다!')
    exit(1)


class Ui_Dialog(object):
    first_flag = 0
    def setupUi(self, Dialog):

        Dialog.setObjectName("Dialog")
        Dialog.resize(800, 480)

        self.tabWidget = QtWidgets.QTabWidget(Dialog)
        self.tabWidget.setGeometry(QtCore.QRect(-4, -1, 811, 481))
        self.tabWidget.setObjectName("tabWidget")
        self.Main = QtWidgets.QWidget()
        self.Main.setObjectName("Main")

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

        self.Enroll = QtWidgets.QWidget()
        self.Enroll.setObjectName("Enroll")
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
        self.numpad8 = QtWidgets.QPushButton(self.Enroll)
        self.numpad8.setGeometry(QtCore.QRect(410, 320, 121, 111))
        self.numpad8.setObjectName("numpad8")
        self.numpad9 = QtWidgets.QPushButton(self.Enroll)
        self.numpad9.setGeometry(QtCore.QRect(540, 320, 121, 111))
        self.numpad9.setObjectName("numpad9")
        self.numpad5 = QtWidgets.QPushButton(self.Enroll)
        self.numpad5.setGeometry(QtCore.QRect(20, 320, 121, 111))
        self.numpad5.setObjectName("numpad5")
        self.numpad_enter = QtWidgets.QPushButton(self.Enroll)
        self.numpad_enter.setGeometry(QtCore.QRect(670, 320, 121, 111))
        self.numpad_enter.setObjectName("numpad_enter")
        self.numpad7 = QtWidgets.QPushButton(self.Enroll)
        self.numpad7.setGeometry(QtCore.QRect(280, 320, 121, 111))
        self.numpad7.setObjectName("numpad7")
        self.numpad6 = QtWidgets.QPushButton(self.Enroll)
        self.numpad6.setGeometry(QtCore.QRect(150, 320, 121, 111))
        self.numpad6.setObjectName("numpad6")
        self.label_enroll = QtWidgets.QLabel(self.Enroll)
        self.label_enroll.setGeometry(QtCore.QRect(20, 30, 771, 131))
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        font.setStrikeOut(False)
        self.label_enroll.setFont(font)
        self.label_enroll.setAutoFillBackground(True)
        self.label_enroll.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.label_enroll.setScaledContents(False)
        self.label_enroll.setAlignment(QtCore.Qt.AlignCenter)
        self.label_enroll.setObjectName("label_enroll")
        self.tabWidget.addTab(self.Enroll, "")
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
        self.numpad_enter.clicked.connect(self.enroll_start)


        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setPointSize(48)
        font.setBold(True)
        font.setWeight(75)
        self.Delete = QtWidgets.QWidget()
        self.Delete.setObjectName("Delete")
        self.tabWidget.addTab(self.Delete, "")
        
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

        self.retranslateUi(Dialog)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):

        _translate = QtCore.QCoreApplication.translate

        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
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
        self.numpad8.setText(_translate("Dialog", "8"))
        self.numpad9.setText(_translate("Dialog", "9"))
        self.numpad5.setText(_translate("Dialog", "5"))
        self.numpad_enter.setText(_translate("Dialog", "확인"))
        self.numpad7.setText(_translate("Dialog", "7"))
        self.numpad6.setText(_translate("Dialog", "6"))

        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Enroll), _translate("Dialog", "등록"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Delete), _translate("Dialog", "삭제"))
        self.label_delete.setText(_translate("Dialog", "삭제"))
        
        self.showtime()
        self.MainMessage()


    def showtime(self):
        # 1970년 1월 1일 0시 0분 0초 부터 현재까지 경과시간 (초단위)
        t = time.time()
        # 한국 시간 얻기
        kor = time.localtime(t)
        # LCD 표시
        clock = str(kor.tm_year) + "-"
        clock += str(kor.tm_mon) + "-"
        clock += str(kor.tm_mday) + "   "
        clock += str(kor.tm_hour) + ":"
        clock += str(kor.tm_min) + ":"
        clock += str(kor.tm_sec)

        limit_time = str(kor.tm_hour)
        limit_time += str(kor.tm_min)
        limit_time += str(kor.tm_sec)
        
        alarm_time = str(kor.tm_hour)
        alarm_time += str(kor.tm_min)
        alarm_time += str(kor.tm_sec)
        #print(limit_time)
        
        if(alarm_time == "235010" or alarm_time == "235510"):
            pygame.mixer.music.play()
        
        if(limit_time == "235810"):
            response = requests.post(URL_Limit)
            print(response.status_code)

        self.label_time.setText(clock)

        #print(self.tabWidget.currentIndex())

        if (self.tabWidget.currentIndex() == 0):
            Main_ID["tabNum"] = "출석"
        elif(self.tabWidget.currentIndex() == 1):
            Enroll_NAME["tabNum"] = "등록"
        elif(self.tabWidget.currentIndex() == 2):
            Main_ID["tabNum"] = "삭제"

        # 타이머 설정  (1초마다, 콜백함수)
        timer = Timer(1, self.showtime)
        timer.start()
        
    def change_state_in(self):
        Main_ID["tab"] = "true"
        print(Main_ID["tab"])
    def change_state_out(self):
        Main_ID["tab"] = "false"
        print(Main_ID["tab"])
    
    def num_input0(self):
        Enroll_NAME["std_num"] += "0"
        self.label_enroll.setText(Enroll_NAME["std_num"])
        print(Enroll_NAME["std_num"])
    def num_input1(self):
        Enroll_NAME["std_num"] += "1"
        self.label_enroll.setText(Enroll_NAME["std_num"])
        print(Enroll_NAME["std_num"])
    def num_input2(self):
        Enroll_NAME["std_num"] += "2"
        self.label_enroll.setText(Enroll_NAME["std_num"])
        print(Enroll_NAME["std_num"])
    def num_input3(self):
        Enroll_NAME["std_num"] += "3"
        self.label_enroll.setText(Enroll_NAME["std_num"])
        print(Enroll_NAME["std_num"])
    def num_input4(self):
        Enroll_NAME["std_num"] += "4"
        self.label_enroll.setText(Enroll_NAME["std_num"])
        print(Enroll_NAME["std_num"])
    def num_input5(self):
        Enroll_NAME["std_num"] += "5"
        self.label_enroll.setText(Enroll_NAME["std_num"])
        print(Enroll_NAME["std_num"])
    def num_input6(self):
        Enroll_NAME["std_num"] += "6"
        self.label_enroll.setText(Enroll_NAME["std_num"])
        print(Enroll_NAME["std_num"])
    def num_input7(self):
        Enroll_NAME["std_num"] += "7"
        self.label_enroll.setText(Enroll_NAME["std_num"])
        print(Enroll_NAME["std_num"])
    def num_input8(self):
        Enroll_NAME["std_num"] += "8"
        self.label_enroll.setText(Enroll_NAME["std_num"])
        print(Enroll_NAME["std_num"])
    def num_input9(self):
        Enroll_NAME["std_num"] += "9"
        self.label_enroll.setText(Enroll_NAME["std_num"])
        print(Enroll_NAME["std_num"])
    def num_back(self):
        Enroll_NAME["std_num"] = ""
        self.label_enroll.setText("학번을 입력해주세요")
        print(Enroll_NAME["std_num"])
    

    def enroll_start(self):
        #Enroll_NAME["std_num"] = self.lineEdit.text()
        #self.lineEdit.clear()
        print(Enroll_NAME["std_num"])
        
        ## POST 통신을 이용하여 DB로 학번을 전송 후 존재 유무 수신
        response = requests.post(URL_Numcheck, data=Enroll_NAME)
       # print(Enroll_NAME)
        ## 돌아오는 존재 유무 값을 받은후 json 형에서 다시 딕셔너리로 변환
        Enroll_FLAG = json.loads(response.text)
        #print(Enroll_FLAG)
        if(Enroll_FLAG["flag_exist"] == "true"):
            prt = Enroll_FLAG["userName"] + "님 지문 등록을 진행합니다\n센서에 손가락을 올려주세요"
            self.label_enroll.setText(prt)
        else:
            self.label_enroll.setText("등록정보가 확인되지 않습니다")
        
        
        
    def setMessage(self,string):
        self.label_text.setText(string)
        
    def MainMessage(self):
        if self.first_flag == 0:   
            while (f.readImage() == False):
                pass
            
            if(self.tabWidget.currentIndex() == 0):
                
                ## 읽은 이미지를 문자열로 변환
                f.convertImage(0x01)

                result = f.searchTemplate()

                positionNumber = result[0]
                score = result[1]
                
                ## 지문 검사
                if (positionNumber == -1): 
                    self.label_text.setText("등록되지 않은 지문입니다")
                    time.sleep(1)
                else:
                    if (score >= 45):
                        Main_ID["primaryKEY"] = str(positionNumber)
                        response = requests.post(URL_Main, data=Main_ID)
                        Main_CHECK = json.loads(response.text)
                       # print(Main_CHECK)
                        #print(Main_ID)
                        
                        # check_in, check_out -> set
                        if(Main_CHECK['data'] == True):
                        
                            # Radiobutton이 입실로 체크, 입실내역이 존재하지 않는 상황
                            if((self.button_in.isChecked() == True) and (Main_CHECK['check'] == False)):
                                prt = Main_CHECK["userName"] + "님 입실처리 되었습니다"
                                self.label_text.setText(prt)
                               # print(Main_CHECK)

                            # Radiobutton이 입실로 체크, 입실 내역이 존재하는 상황
                            elif((self.button_in.isChecked() == True) and (Main_CHECK['check'] == True)):
                                self.label_text.setText("입/퇴실 버튼을 확인하세요")
                                """
                                msg = QMessageBox()
                                msg.setWindowTitle("입퇴실 확인")
                                msg.setText("입실내역 O \n 퇴실하시겠습니까?")
                                msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                                x = msg.exec()
                                
                                if(x == QMessageBox.Yes):
                                    self.button_out.setChecked(True)
                                    prt = Main_CHECK["userName"] + "님 퇴실처리 되었습니다"
                                    self.setMessage(prt)
                                    print(Main_CHECK)
                                else:
                                    prt = ("입실 퇴실 체크를 올바르게 해주세요")
                                    self.setMessage(prt)
                                    print(Main_CHECK)
                                """
                            # Radiobutton이 퇴실로 체크, 입실내역이 존재하지 않는 상황
                            elif((self.button_out.isChecked() == True) and (Main_CHECK['check'] == False)):
                                self.label_text.setText("입/퇴실 버튼을 확인하세요")
                                """
                                msg = QMessageBox()
                                msg.setWindowTitle("입퇴실 확인")
                                msg.setText("입실내역X\n입실하시겠습니까?")
                                msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                                x = msg.exec()
                                
                                if (x == 16384):
                                    self.button_out.setChecked(True)
                                    prt = (Main_CHECK["userName"] + "님 입실처리 되었습니다")
                                    self.setMessage(prt)
                                    print(Main_CHECK)
                                else:
                                    self.label_text.setText("입실 퇴실 체크를 올바르게 해주세요")
                                    print(Main_CHECK)
                                """
                            # Radiobutton이 퇴실로 체크, 입실내역이 존재하는 상황
                            elif((self.button_in.isChecked() == False) and (Main_CHECK['check'] == True)):
                                prt = (Main_CHECK["userName"] + "님 퇴실처리 되었습니다")
                                self.setMessage(prt)
                        else:
                            self.label_text.setText("이미 입/퇴실 완료되었습니다.\n또는 입/퇴실 버튼을 확인하세요")
                                
                            

                    else:
                        self.label_text.setText("다시 인증해주세요")
            elif(self.tabWidget.currentIndex() == 1):
                
                ## 읽은 이미지를 문자열로 변환
                f.convertImage(0x01)

                result = f.searchTemplate()

                positionNumber = result[0]
                        
                score = result[1]
                self.label_enroll.setText("센서에 다시 손가락을 올려주세요")
                
                ## 다시 손가락을 올릴 때 까지 대기
                while ( f.readImage() == False ):
                    pass

                ## 읽은 이미지를 문자열로 변환
                f.convertImage(0x02)
                
                ## 지문정보를 비교, 이미 등록된 지문인 경우
                if (positionNumber >= 0):
                    self.label_enroll.setText("이미 등록된 지문 입니다")
                    
                ## 지문정보를 비교, 정확도가 낮은 경우
                elif (f.compareCharacteristics() == 0):
                    self.label_enroll.setText("정확도가 낮습니다\n조금 더 정확하게 찍어주세요")
                    
                ## 등록된 지문이 아니고, 정확도가 높은 경우
                else:
                    ## 지문틀 생성
                    f.createTemplate()

                    ## 지문을 저장하고 번호 부여
                    positionNumber = f.storeTemplate()
                    
                    Enroll_ID["primaryKEY"] = positionNumber
                    Enroll_ID["userID"] = Enroll_NAME["std_num"]
                    Enroll_NAME["std_num"] = ""
                    #print(Enroll_ID)
                    response = requests.post(URL_Enroll, data=Enroll_ID)
                    Enroll_FLAG = json.loads(response.text)
                    #print(Enroll_FLAG)
                    prt = Enroll_FLAG["userName"] + "님 지문등록 성공"
                    self.label_enroll.setText(prt)
                
            else:
                ## 읽은 이미지를 문자열로 전환
                f.convertImage(0x01)
                         
                ## 등록된 지문인지 확인 후 지문넘버 저장
                result = f.searchTemplate()
                positionNumber = result[0]
                
                ## 지문 넘버에 따른 진행과정
                if ( positionNumber >= 0 ):
                    Delete_ID["primaryKEY"] = str(positionNumber)
                    f.deleteTemplate(positionNumber)
                    
                    response = requests.post(URL_Delete, data=Delete_ID)
                    print(Delete_ID)
                    print(response.status_code)
                    self.label_delete.setText("지문이 삭제되었습니다")
                else:
                    self.label_delete.setText("지문정보가 잘못되었습니다")
                    
            timer = Timer(1, self.sensor)
            timer.start()
    

    def sensor(self):
        self.MainMessage()
        #t = threading.Timer(1, self.sensor)
        #t.start()
    

#t = threading.Timer(1, Ui_Dialog.sensor)
#t.start()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.showFullScreen()
    sys.exit(app.exec_())


