import socket
import cv2
import numpy
from  queue import Queue
from  _thread import *
import tkinter as tk
import serial
import time
import threading
import base64
import pymysql


def parking_check():
    con = pymysql.connect(host="localhost",
                          user='root',
                          password='176688',
                          db="jucha_db",
                          charset='utf8'
                          )
    cur = con.cursor()
    ppl = f"""SELECT car_number FROM jucha_db.parking_in;"""
    # self.cur.execute(use)
    cur.execute(ppl)
    data = list(cur.fetchall())
    return data

def parking_join(number):
    con = pymysql.connect(host="localhost",
                          user='root',
                          password='176688',
                          db="jucha_db",
                          charset='utf8'
                          )

    ppl = f"""insert into jucha_db.parking_in values (NULL,'{number}',1,'2023-02-09');"""
    with con:
        with con.cursor() as cur:
            cur.execute(ppl)
            con.commit()
            cur.close()
    return



data2 = ''

aduino_number = ''

enclosure_queue=Queue()

py_serial = serial.Serial(port='COM1',baudrate=9600)

def aduino():
    global data2
    global aduino_number
    while True:
        response = py_serial.readline()
        bbb= response.decode()
        #print(type(bbb))
        bbb = bbb.replace("\r",'')
        bbb = bbb.replace('\n','')
        #print(bbb)
        if len(bbb) == 1:
            if len(aduino_number) < 4:
                aduino_number = aduino_number + bbb
            elif len(aduino_number) >= 4:
                aduino_number=aduino_number[1:]+bbb
        if bbb == '24946':
            aduino_number = aduino_number[:-1]

        elif bbb == '25964':
            aduino_number =''

        elif bbb == '26990':
            print("번호 조회")
            a= []
            bb = parking_check()
            for i in bb:
                a.append(i[0])
            #if len(aduino_number) == 4:
            if aduino_number not in a:
                parking_join(aduino_number)
                print("차량등록 완료")
                print("현재 등록된 차량 : ", parking_check())
                aduino_number = ""
            else:
                print("이미 등록된 번호 입니다.")

           # else:
                #print("차량번호는 4자리만 등록가능 합니다.")

        print("차량번호 : ",aduino_number)

receive_thread = threading.Thread(target=aduino)
receive_thread.daemon = True
receive_thread.start()


def threaded(client_socket,addr,queue):
    global data2
    print("연결 주소:",addr[0],"-",addr[1])
    while True:
        try:
            data = client_socket.recv(1024)

            if not data:
                print("연결해제",addr[0],"-",addr[1])
                break


            if "aduino open" in data.decode():
                py_serial.write("a".encode())

            elif "aduino close" in data.decode():
                py_serial.write("s".encode())

            elif "aduino end" in data.decode():
                py_serial.write("d".encode())

            elif "check" in data.decode():
                bbb= data.decode()
                bbb = str(bbb[6:])
                bbb= bbb.strip()
                print(bbb)
                bb = parking_check()
                for i in bb:
                    if bbb == i[0]:
                        #print("zzzz")
                        py_serial.write("a".encode())

                #print(bb)


            stringData = queue.get()
            client_socket.send(str(len(stringData)).ljust(16).encode()) # ljust 바이너리데이터 민칸 매꾸는 함수(규격을맞추기위한사용)
            client_socket.send(stringData)

        except:
            print("error")
            break
    client_socket.close()


def webcam(queue):
    capture = cv2.VideoCapture(0)
    go = True
    count = 0
    while True:
        ret,frame =capture.read()
        if ret == False:

            continue

        encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),90]
        result,imgencode = cv2.imencode('.jpg',frame,encode_param)
        data = numpy.array(imgencode)
        byteData = data.tobytes()

        if go == True:
            #print(data.shape)
            for i in byteData:
                #print(i)
                count+=1

            #print(count, "카운트 숫자")
            go=False

        byteData=data.tobytes()#numpy에 재공하는 바이트 변환 함수
        queue.put(byteData)
        cv2.imshow("gray_frame",frame)
        key = cv2.waitKey(1)
        #if key ==ord('s'):
            #break
        if key ==27:
            break


print("키패드 사용법")
print("* : 차량등록")
print("A : 강제 문개방")
print("B : 강제 문 닫기")
print("C : 등록할 차량번호 한개 삭제")
print("D : 등록할 차량번호 전체 삭제")

print()
HOST = '192.168.0.61'
PORT = 9900

server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
server_socket.bind((HOST,PORT))
server_socket.listen()
print("server on")

start_new_thread(webcam,(enclosure_queue,))


while True:
    print("클라이언트 접속 대기 while 문")
    client_socket , addr  = server_socket.accept()
    start_new_thread(threaded,(client_socket,addr,enclosure_queue,))



server_socket.close()
