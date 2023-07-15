import cv2
import pandas as pd
# import numpy as np
from ultralytics import YOLO
from tracker import *
import cvzone

def RGB(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE :  
        point = [x, y]
        print(point)
    
            

def fun(): 
    model = YOLO("yolov8s.pt")
    #  function to track the mouse coordinates
    cv2.namedWindow('RGB')
    cv2.setMouseCallback('RGB', RGB)
    cap=cv2.VideoCapture('static\\files\\vidp.mp4')
    my_file = open("coco.txt", "r")
    data = my_file.read()
    class_list = data.split("\n")
    count=0
    persondown={}
    tracker=Tracker()
    counter1=[]
    personup={}
    counter2=[]
    cy1=194
    cy2=220
    offset=6
    while True:    
        ret,frame = cap.read()
        if not ret:
            break
        count += 1
        if count % 3 != 0:
            continue
        frame=cv2.resize(frame,(1020,500))
    

        results=model.predict(frame)
        a=results[0].boxes.data
        px=pd.DataFrame(a).astype("float")
        list=[]
    
        for index,row in px.iterrows():
            x1=int(row[0])
            y1=int(row[1])
            x2=int(row[2])
            y2=int(row[3])
            d=int(row[5])
            
            c=class_list[d]
            if 'person' in c:

                list.append([x1,y1,x2,y2])
        
            
        bbox_id=tracker.update(list)
        for bbox in bbox_id:
            x3,y3,x4,y4,id=bbox
            cx=int(x3+x4)//2
            cy=int(y3+y4)//2
            cv2.circle(frame,(cx,cy),4,(255,0,255),-1)
            cv2.rectangle(frame,(x3,y3),(x4,y4),(0,0,255),2)
            cvzone.putTextRect(frame,f'{id}',(x3,y3),1,2)
            if cy1<(cy+offset) and cy1>(cy-offset):
                cv2.rectangle(frame,(x3,y3),(x4,y4),(0,255,0),2)
                cvzone.putTextRect(frame,f'{id}',(x3,y3),1,2)
                persondown[id]=cy
                if id in personup:
                    if counter2.count(id)==0:
                        counter2.append(id)
            if cy2<(cy+offset) and cy2>(cy-offset):
                cv2.rectangle(frame,(x3,y3),(x4,y4),(0,255,255),2)
                cvzone.putTextRect(frame,f'{id}',(x3,y3),1,2)
                personup[id]=cy
                if id in persondown:
                    if counter1.count(id)==0:
                        counter1.append(id)
        cv2.line(frame,(3,cy1),(1018,cy1),(0,255,0),2)
        cv2.line(frame,(5,220),(1019,220),(0,255,255),2)
    #    /meausrement of line using cursor
        down = len(counter1)
        up = len(counter2)
        cvzone.putTextRect(frame,f'Down{down : }',(10,50),1,2)
        cvzone.putTextRect(frame,f'Up{up : }',(10,100),1,2)
        cv2.imshow("RGB", frame)
        if cv2.waitKey(1)&0xFF==27:
            break
    cap.release()
    cv2.destroyAllWindows()

# fun()