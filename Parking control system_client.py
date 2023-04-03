import socket
import tkinter as tk
import numpy as np
from tkinter import *
import cv2  # OpenCV
import PIL.Image, PIL.ImageTk
import threading  # Thread
import datetime
from queue import Queue
import pandas as pd
import serial
import time
import pytesseract
from PIL import Image
from collections import Counter
import queue
#py_serial = serial.Serial(port='COM5',baudrate=9600)

comand =""

# def aduino():
#     global comand
#     while True:
#         py_serial.write(comand.encode())
#         time.sleep(0.1)
#         if py_serial.readable():
#             # 들어온 값이 있으면 값을 한 줄 읽음 (BYTE 단위로 받은 상태)
#             # BYTE 단위로 받은 response 모습 : b'\xec\x97\x86\xec\x9d\x8c\r\n'
#             response = py_serial.readline()
#
#             # 디코딩 후, 출력 (가장 끝의 \n을 없애주기위해 슬라이싱 사용)
#             print(response[:len(response) - 1].decode())
#
#
# receive_thread = threading.Thread(target=aduino)
# receive_thread.daemon = True
# receive_thread.start()


HOST = '192.168.0.61'
PORT = 9900
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))
count = 0
vid = 0
a = 0
leri = 0
data1 = 0
chec = 0
open1 = 0
aaa= 0

teccc= 0
tec1 = 0
q_test =0


ret =None
draw = None
a1,a2,a3 = None,None,None
cap123 = None

vv1 = False
low = False
end = None
q_start=None

check_recv = 0
car_number =None


frame_self = 0

def recvall(sock, count):

    buf = b''
    while count:
        newbuf = sock.recv(count)

        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf


def massage():
    global data1
    global teccc
    global tec1
    global q_test
    global a1
    global a2
    global a3
    global ret
    global draw
    global cap123
    global q_start
    global check_recv
    global comand

    cap1= datetime.datetime.now()
    cap2 = cap1.second
    cap22 = cap1.second
    q_test = Queue()
    meme=1
    count = 0
    while True:

        message = '1'

        client_socket.send(message.encode())
        length = recvall(client_socket, 16)

        stringData = recvall(client_socket, int(length))
        data = np.frombuffer(stringData, dtype='uint8')

        data1 = cv2.imdecode(data, 1)

        comand =''


        if count ==0:
            receive_thread2.start()
            count +=1


receive_thread = threading.Thread(target=massage)
receive_thread.daemon = True
receive_thread.start()


def self_photo():
    global frame_self

    capture11 = cv2.VideoCapture(0)
    while True:
        ret,frame_self = capture11.read()


receive_thread2 = threading.Thread(target=self_photo)
receive_thread2.daemon = True
#receive_thread2.start()


pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'


class Recognition:
    def ExtractNumber(self):
        try:
            Number = 'test.jpg'
            img = cv2.imread(Number, cv2.IMREAD_COLOR)
            copy_img = img.copy()
            img2 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            cv2.imwrite('gray.jpg', img2)
            blur = cv2.GaussianBlur(img2, (3, 3), 0) # 가우시안 블러 노이즈 줄이기
            cv2.imwrite('blur.jpg', blur)
            canny = cv2.Canny(blur, 100, 200) # 윤곽선 구분 전처리
            cv2.imwrite('canny.jpg', canny)
            contours, hierarchy = cv2.findContours(canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            box1 = []
            f_count = 0
            select = 0
            plate_width = 0

            for i in range(len(contours)): #
                cnt = contours[i]
                area = cv2.contourArea(cnt)
                x, y, w, h = cv2.boundingRect(cnt)
                rect_area = w * h  # area size
                aspect_ratio = float(w) / h  # ratio = width/height

                if (aspect_ratio >= 0.1) and (aspect_ratio <= 1.0) and (rect_area >= 100) and (rect_area <= 1200):
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 1)
                    box1.append(cv2.boundingRect(cnt))

            for i in range(len(box1)):  ##Buble Sort on python
                for j in range(len(box1) - (i + 1)):
                    if box1[j][0] > box1[j + 1][0]:
                        temp = box1[j]
                        box1[j] = box1[j + 1]
                        box1[j + 1] = temp

            # to find number plate measureing length between rectangles
            for m in range(len(box1)):
                count = 0
                for n in range(m + 1, (len(box1) - 1)):
                    delta_x = abs(box1[n + 1][0] - box1[m][0])
                    if delta_x > 150:
                        break
                    delta_y = abs(box1[n + 1][1] - box1[m][1])
                    if delta_x == 0:
                        delta_x = 1
                    if delta_y == 0:
                        delta_y = 1
                    gradient = float(delta_y) / float(delta_x)
                    if gradient < 0.25:
                        count = count + 1
                # measure number plate size
                if count > f_count:
                    select = m
                    f_count = count;
                    plate_width = delta_x
            cv2.imwrite('snake.jpg', img)
            # 10:box1[select][3] + box1[select][1] + 20
            number_plate = copy_img[box1[select][1] - 30:box1[select][3] + box1[select][1] + 50,
                           box1[select][0] - 10:140 + box1[select][0]]
            resize_plate = cv2.resize(number_plate, None, fx=1.3, fy=1.3, interpolation=cv2.INTER_CUBIC + cv2.INTER_LINEAR)
            plate_gray = cv2.cvtColor(resize_plate, cv2.COLOR_BGR2GRAY)
            ret, th_plate = cv2.threshold(plate_gray, 150, 255, cv2.THRESH_BINARY) # 색 굵기

            cv2.imwrite('plate_th.jpg', th_plate)
            kernel = np.ones((2, 3), np.uint8)
            er_plate = cv2.erode(th_plate, kernel, iterations=1)
            er_invplate = er_plate
            cv2.imwrite('er_plate.jpg', er_invplate)
            result = pytesseract.image_to_string(Image.open('er_plate.jpg'), lang='kor',config='digits') #config='digits'
            return (result.replace(" ", ""))
        except:
            pass

class log_main(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.geometry("1500x800")
        self._frame = None
        self.switch_frame(StartPage)

    def switch_frame(self, frame_class):
        self.geometry("1500x800")
        new_frame = frame_class(self)

        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame

    def next_frame(self, frame_class):
        self.geometry("1500x800")
        new_frame = frame_class(self)

        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame

class StartPage(tk.Frame):  # 첫화면 프레임
    back = None
    canvas1 = None
    close = None
    open1 = None
    canvas2 = None

    def __init__(self, master):
        global open1
        global aaa
        tk.Frame.__init__(self, master, bg="white", width=1600, height=800)
        tk.Frame.place(self, x=38, y=30)

        #self.open1 = tkinter.BooleanVar()
        #self.open1.set(False)
        self.canvas1 = tk.Canvas(self, width=650, height=750,bg='white')
        self.canvas1.place(x=10,y=20)

        self.canvas2 = tk.Canvas(self, width=650, height=750,bg='white')
        self.canvas2.place(x=700,y=20)

        self.cap = cv2.VideoCapture(0)

        # self.delay = 1
        # self.update()
        k = tk.Button(self, width=10, height=2, text="메인",command=self.start)
        k.place(x=50,y=500)

        # a=tk.Button(self, width=10, height=2, text="슈렉필터",command=self.aaa)
        # a.place(x=150,y=500)
        #
        # b=tk.Button(self, width=10, height=2, text="흑백",command=self.bbb)
        # b.place(x=250,y=500)
        #
        # c=tk.Button(self, width=10, height=2, text="수채화",command=self.ccc)
        # c.place(x=350,y=500)
        #
        # d = tk.Button(self, width=10, height=2, text="애니메이션", command=self.ddd)
        # d.place(x=50, y=550)

        # e = tk.Button(self, width=10, height=2, text="트래킹", command=lambda :master.next_frame(motion_tracking))
        # e.place(x=150, y=550)

        ddd = tk.Button(self, width=10, height=2, text="열려라")
        ddd.bind("<Button-1>", self.aduino_open)
        ddd.place(x=250, y=550)

        bbb = tk.Button(self, width=10, height=2, text="닫혀라")
        bbb.bind("<Button-1>", self.aduino_close)
        bbb.place(x=350, y=550)

        ccc = tk.Button(self, width=10, height=2, text="초기화")
        ccc.bind("<Button-1>", self.aduino_clear)
        ccc.place(x=450, y=550)


        self.delay = 30
        self.update() #서버
        #self.motion_T()
        self.my_photo() #본인 웹캠

    def aduino_open(self, e):
        global comand
        global car_number
        #global check_recv

        self.capcure()
        print(car_number,"aduino_open")

        comand = f"check {car_number}"
        client_socket.send(comand.encode())
        comand = ''
        car_number = ""
    def aduino_close(self, e):
        global comand
        comand = "aduino close"
        client_socket.send(comand.encode())
        #time.sleep(0.1)
        comand = ""
        #client_socket.send("aduino: s".encode())


    def aduino_clear(self, e):
        global comand

        comand = "aduino end"
        client_socket.send(comand.encode())
        #time.sleep(0.1)
        comand = ""
        #client_socket.send("aduino: d".encode())

    def capcure(self):
        global frame_self
        global car_number
        try:
            testaa= []
            for i in range(50):
                cv2.imwrite("test.jpg",frame_self)

                recogtest = Recognition()
                result = recogtest.ExtractNumber()
                result = str(result)[:-2]
                if result.isdigit():
                    if len(result) == 4:
                        print(result,"isdigit 되는지 확인")
                        testaa.append(result)

            conter = Counter(testaa)
            print(conter,"캡처구간")
            car_number = max(conter, key=conter.get)

        except Exception as e:
            print(e)
            pass


    def start(self):
        global a
        a=0

    def aaa(self):
        global a
        a=1

    def bbb(self):
        global a
        a = 2

    def ccc(self):
        global a
        a = 3

    def ddd(self):
        global a
        a=4

    def chec(self):
        global aaa
        if self.open1.get() == True:
            aaa=1
        else:
            aaa=0

    def my_photo(self): #본인웹캠

        global frame_self

        try:

            frame = cv2.cvtColor(frame_self, cv2.COLOR_BGR2RGB)

            self.photo1 = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
            self.canvas2.create_image(0, 0, image=self.photo1, anchor=NW)
            #print(frame)


            self.after(self.delay, self.my_photo)
        except Exception as a :
            print(a)
            self.after(self.delay, self.my_photo)


    def motion_T(self): #모션 확인 함수
        global tec1
        global data1
        global teccc
        global a1
        global a2
        global a3
        global ret

        thresh = 25  # 픽셀 차
        max_diff = 5

        a_gray = cv2.cvtColor(data1, cv2.COLOR_BGR2GRAY) # 무한
        b_gray = cv2.cvtColor(a2, cv2.COLOR_BGR2GRAY) # 2초 후
        c_gray = cv2.cvtColor(a3, cv2.COLOR_BGR2GRAY) # 3초 후
        draw = a_gray.copy()

        diff1 = cv2.absdiff(b_gray, a_gray)
        diff2 = cv2.absdiff(c_gray, a_gray)

        ret, diff1_t = cv2.threshold(diff1, thresh, 255, cv2.THRESH_BINARY)
        ret, diff2_t = cv2.threshold(diff2, thresh, 255, cv2.THRESH_BINARY)

        diff = cv2.bitwise_and(diff1_t, diff2_t)

        k = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))

        diff = cv2.morphologyEx(diff, cv2.MORPH_OPEN, k)

        diff_cnt = cv2.countNonZero(diff)

        if diff_cnt > max_diff:
            nzero = np.nonzero(diff)
            cv2.rectangle(draw, (min(nzero[1]), min(nzero[0])), (max(
                nzero[1]), max(nzero[0])), (0, 255, 0), 2)

            cv2.putText(draw, "Motion detected!", (10, 30),
                       cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 0, 255))




        draw = cv2.cvtColor(draw, cv2.COLOR_GRAY2BGR)
        stacked = np.hstack((draw, cv2.cvtColor(diff, cv2.COLOR_GRAY2BGR)))
        self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(stacked))
        self.canvas1.create_image(0, 0, image=self.photo, anchor=NW)

        #if self.open1 == True:

        self.after(self.delay,self.motion_T)


    def update(self):
        global data1
        global a
        global open1
        global teccc
        global tec1
        global q_test
        global zero
        try:

            if a == 0:


                vid = cv2.cvtColor(data1, cv2.COLOR_BGR2RGB)
                self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(vid))

            self.canvas1.create_image(0, 0, image=self.photo, anchor=NW)

        except Exception as e:
            #print(e)
            pass
        self.after(self.delay, self.update)

    def vvvvv(self): # 녹화 시작을 위한 함수
        global vv1
        global low
        vv1 =True
        low =True
        self.time()
        self.q_start()
        receive_thread1.start()


    def time(self): # 10초 녹화를 위한 타임 함수
        global end
        end = datetime.datetime.now().second

    def q_start(self): #queue 에 쌓기 위한 트루펄스
        global q_start
        q_start=True




def video(): #녹화 쓰레드를 돌리기 위한 함수
    #global data1
    global vv1
    global low
    global end
    global q_test
    global q_start
    global frame_self
    #print(end)
    print("녹화시작")
    while True:
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        now = datetime.datetime.now().strftime("%d_%H-%M-%S")
        start = datetime.datetime.now().second

        if vv1==True:
            video = cv2.VideoWriter("D:/ChoPython/2023년/녹화/" + str(now) + ".avi", fourcc, 20.0,
                                    (frame_self.shape[1], frame_self.shape[0]))
            vv1 =False
        elif end + 10 == start:
            print("녹화 끝")
            low =False
            q_start=False
            receive_thread1.stop()
            break
        if low == True:
            video.write(q_test.get())


receive_thread1 = threading.Thread(target=video)
receive_thread1.daemon = True



def start():
    if __name__ == "__main__":
        global app
        app = log_main()
        app.geometry("1500x800")
        app.resizable(False, False)
        app.configure(bg="white")
        app.mainloop()

start()










