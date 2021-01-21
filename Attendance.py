import tkinter as tk #gui lib
from tkinter import Message ,Text #notifiations
import cv2,os #computer vision #OS lib for path handling   
import shutil #fast file operation lib -copy - move -open - close
import csv #reading csv and writing csv
import numpy as np #numeric python normally for array
from PIL import Image, ImageTk #pilow image module for fast image processing
from PIL import ImageFilter
import pandas as pd #data management 
import datetime #for attendance timing 
import time #for attendance timing
import tkinter.ttk as ttk #themed widgets
import tkinter.font as font #font formating

window = tk.Tk() #initialize the window
window.title("Attendance System")
window.geometry("565x700")
window.configure(background='gray61')
# --------
# ------------------------------------------# functions -start
def remove():
    if len(os.listdir("DATA\Images"))!=0:
        Id=(txt.get())
        if(is_number(Id) and removecheck(Id)):
            if len(os.listdir("DATA\Images"))==0:
                res = "no data to delete"
                message.configure(text= res)
            else:
                imgnames=os.listdir("DATA\Images")
                imgnum=0
                for title in imgnames:
                    parts=title.split(".")
                    if parts[1]==Id:
                        imgnum+=1
                        if imgnum==40:
                            print("--------------------Remove Process")
                            print ("Removed - 'Name': " +parts[0]+ " And 'ID': " +parts[1])
                        os.remove("DATA/Images/"+title)
                print("process complete")
                f= open("DATA\Registration\Temp.csv","w+")
                f.close()
                file1 = open("DATA\Registration\StudentDetails.csv", 'r')
                reader = csv.reader(file1)
                new_rows_list = []
                for row in reader:
                    if len(row)!=0:
                        if row[0] != Id :
                            new_rows_list.append(row)
                print("-------------------------Current items in StudentDetails.csv")
                for element in new_rows_list:
                    print(element)
                print("-------------------------End Of StudentDetails.csv")
                file1.close() 
                file2 = open("DATA\Registration\Temp.csv", 'a+')
                writer = csv.writer(file2)
                writer.writerows(new_rows_list)
                file2.close()
                os.remove("DATA\Registration\StudentDetails.csv")
                os.rename("DATA\Registration\Temp.csv", "DATA\Registration\StudentDetails.csv")
                #result--below
                res = "Removed -please train the model now"
                message.configure(text= res)
                if len(os.listdir("DATA\model"))!=0:
                    os.remove("DATA\model\model.yml")

        else:
                file1 = open("DATA\Registration\StudentDetails.csv", 'r')
                reader = csv.reader(file1)
                new_rows_list = []
                for row in reader:
                    if len(row)!=0:
                        new_rows_list.append(row)
                print("-------------------------Current items in StudentDetails.csv")
                for element in new_rows_list:
                    print(element)
                print("-------------------------End Of StudentDetails.csv")
                file1.close() 
                res = "invalid id"
                message.configure(text = res)
                # print("test ext")
    else:
        file1 = open("DATA\Registration\StudentDetails.csv", 'r')
        reader = csv.reader(file1)
        new_rows_list = []
        for row in reader:
            if len(row)!=0:
                new_rows_list.append(row)
        print("-------------------------Current items in StudentDetails.csv")
        for element in new_rows_list:
            print(element)
        print("-------------------------End Of StudentDetails.csv")
        file1.close()         
        if len(os.listdir("DATA\model"))!=0:
            os.remove("DATA\model\model.yml")
        res = "Nothing to Remove"
        message.configure(text = res)


def clear(): #removes current form data 
    txt.delete(0, 'end')    
    # res = ""
    # message.configure(text= res)


def clear2(): #removes current form data
    txt2.delete(0, 'end')    
    # res = ""
    # message.configure(text= res)    
    


def getImgData(path):
    imagePaths=[os.path.join(path,f) for f in os.listdir(path)]
    faces=[]
    Ids=[]
    for imagePath in imagePaths:
        pilImage=Image.open(imagePath).convert('L')
        # print(pilImage) 
        imageNp=np.array(pilImage,'uint8')
        Id=int(os.path.split(imagePath)[-1].split(".")[1])
        faces.append(imageNp)
        Ids.append(Id)        
    return faces,Ids
 
def is_number(s): #integer/float check
    try:
        float(s)
        return True
    except ValueError:
        pass
 
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
 
    return False

def existalready(Id):
        imgnames=os.listdir("DATA\Images")
        for title in imgnames:
            parts=title.split(".")
            if parts[1]==Id:
                return False
        return True

def removecheck(Id):
    if existalready(Id) is True:
        return False
    else:
        return True

def capture():        
    Id=(txt.get())
    name=(txt2.get())
    if len(Id)!=0 and len(name)!=0:
        if(is_number(Id) and existalready(Id)):  #numeric-id check
            cam = cv2.VideoCapture(0)          #camera
            HarrPath = "DATA/faces.xml"       #face detector file 
            detector=cv2.CascadeClassifier(HarrPath) #cv2 face detector
            imgnum=0
            while(True):
                ret, img = cam.read()
                iy=int(img.shape[0]/4)
                ix=int(img.shape[1]/4)
                fy=int(img.shape[0]/4)*3
                fx=int(img.shape[1]/4)*3
                grayImg = cv2.cvtColor(img[iy:fy,ix:fx], cv2.COLOR_BGR2GRAY) #convert rgb to grayscale
                # time.sleep(100)
                faces = detector.detectMultiScale(grayImg,scaleFactor=1.1,minNeighbors=7,minSize=(100, 100)) 
                for (x,y,w,h) in faces:
                    cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)     #rectangle with width height   
                    imgnum=imgnum+1   #incrementing sample num 
                    print("imag no : "+ str(imgnum))
                    number = imgnum/10
                    # if number < 1:
                    #     number = 0.7
                    # gray = cv2.convertScaleAbs(grayImg, alpha=float(number), beta=float(number)*5)
                    # kernel = np.array([[-1,-1,-1],[-1, 9,-1],[-1,-1,-1]])
                    # sharp = cv2.filter2D(grayImg, -1, kernel)
                    xx=int(x/10)
                    yy=int(y/10)
                    cv2.imwrite("DATA\Images\ "+name +"."+Id +'.'+ str(imgnum) + ".jpg", grayImg[y-yy:y+h+yy,x-xx:x+w+xx])


                    cv2.imshow('frame',grayImg)
                if cv2.waitKey(1) & 0xFF == ord('q'): #press q to exit to the camera frame
                    break #braek to while loop
                if imgnum>=180:
                    break #if total samples are more then 180 the break the loop
            cam.release() #turning of the camera
            cv2.destroyAllWindows() #closing the camera window
            # res = "Images Saved for ID : " + Id +" Name : "+ name #result variable for notification
            row = [Id , name]
            lists=os.listdir('DATA\Registration')
            if 'StudentDetails.csv' in lists:
                with open('DATA\Registration\StudentDetails.csv','a+') as Datasheet:
                    writer = csv.writer(Datasheet)
                    writer.writerow(row)
                Datasheet.close()
                res = "Person added"
                message.configure(text= res)
            else:
                with open('DATA\Registration\StudentDetails.csv','a+') as Datasheet:
                    writer = csv.writer(Datasheet)
                    writer.writerow(['Id','Name'])
                    writer.writerow(row)
                    Datasheet.close()
                    res = "Person added"
                Datasheet.close()
        else:
            if(name.isalpha()):
                res = "Enter Unieque and Numeric Id"
                message.configure(text= res)
    else:
        res = "Enter Conplete Data"
        message.configure(text= res)


def TrainModel():
    if len(os.listdir("DATA\Images"))==0:
        if len(os.listdir("DATA\model"))!=0:
            os.remove("DATA\model\model.yml")
        res = "no data to train"
        message.configure(text = res)
        return False
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    # recognizer = cv2.face.LBPHFaceRecognizer()
    HarrPath = "DATA/faces.xml"                      # for face detection
    detector =cv2.CascadeClassifier(HarrPath)   #created a detector
    faces,Id = getImgData("DATA\Images")         #geting image label data face,id
    recognizer.train(faces, np.array(Id))             #initializing training using recogniizer 
    recognizer.save("DATA\model\model.yml")     #saving the output trained data
    res = "Model Trained"
    message.configure(text = res)               #printing notification



def TakeAtten():
    if len(os.listdir("DATA\model"))!=0:
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.read("DATA\model\model.yml")
        HarrPath = "DATA/faces.xml"
        HarrFace = cv2.CascadeClassifier(HarrPath);    
        df=pd.read_csv("DATA\Registration\StudentDetails.csv")
        cam = cv2.VideoCapture(0)
        font = cv2.FONT_HERSHEY_SIMPLEX        
        col_names =  ['Id','Name','Date','Time']
        attendance = pd.DataFrame(columns = col_names)    
        number=0
        res = "Press q to Stop Taking Attendance"
        message.configure(text = res)
        while True:
            ret, im =cam.read()
            iy1=int(im.shape[0]/4)
            ix1=int(im.shape[1]/4)
            fy1=int(im.shape[0]/4)*3
            fx1=int(im.shape[1]/4)*3
            gray=cv2.cvtColor(im[iy1:fy1,ix1:fx1],cv2.COLOR_BGR2GRAY)
            faces=HarrFace.detectMultiScale(gray,scaleFactor=1.1,minNeighbors=7,minSize=(100, 100))
            for(x,y,w,h) in faces:
                cv2.rectangle(gray,(x,y),(x+w,y+h),(225,0,0),2)
                number+=1
                # kernel = np.array([[-1,-1,-1],[-1, 9,-1],[-1,-1,-1]])
                # sharp = cv2.filter2D(gray, -1, kernel)
                Id, conf = recognizer.predict(gray[y:y+h,x:x+w])
                conf=100-conf
                print (conf)                             
                if(conf > 50):
                    ts = time.time()      
                    date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y-')
                    timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                    aa=df.loc[df['Id'] == Id]['Name'].values #id name 
                    tt=str(Id)+"-"+aa
                    attendance.loc[len(attendance)] = [Id,aa,date,timeStamp]
                    
                else:
                    Id='Unknown'                
                    tt=str(Id)       
                cv2.putText(gray,str(tt),(x,y+h), font, 1,(255,255,255),2)        
            attendance=attendance.drop_duplicates(subset=['Id'],keep='first')    
            cv2.imshow('image',gray) 
            if (cv2.waitKey(1)==ord('q')):
                break
        ts = time.time()      
        date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
        timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
        Hour,Minute,Second=timeStamp.split(":")
        fileName="DATA\Attendance\Attendance_"+date+"_"+Hour+"-"+Minute+"-"+Second+".csv"
        attendance.to_csv(fileName,index=False)
        cam.release()
        cv2.destroyAllWindows()
        res=attendance
        message2.configure(text= res)
    else:
        res = "Model Not Found"
        message.configure(text = res)



# ------------------------------------------# window-elements
x_ch=0
y_ch=-280
lbl = tk.Label(window, text="Enter ID",width=8  ,height=1  ,fg="gray1"  ,bg="snow" ,font=('times', 15, ' bold ') ) 
txt = tk.Entry(window,width=30  ,bg="snow" ,fg="gray1",font=('times', 15, ' bold '))
lbl2 = tk.Label(window, text="Enter Name",width=8  ,fg="gray1"  ,bg="snow"    ,height=1 ,font=('times', 15, ' bold ')) 
txt2 = tk.Entry(window,width=30  ,bg="snow"  ,fg="gray1",font=('times', 15, ' bold ')  )
lbl3 = tk.Label(window, text="Notice: ",width=8  ,fg="gray1"  ,bg="snow"  ,height=1 ,font=('times', 15, ' bold underline ')) 
lbl3.place(x=10, y=180)
message = tk.Label(window, text="" ,bg="snow"  ,fg="gray1"  ,width=34  ,height=1, activebackground = "yellow" ,font=('times', 15, ' bold ')) 
lbl3 = tk.Label(window, text="Attendance : ",width=45  ,fg="gray1"  ,bg="snow"  ,height=1 ,font=('times', 15, ' bold  underline')) 
message2 = tk.Label(window, text="" ,fg="gray1"   ,bg="snow",activeforeground = "green",width=77  ,height=25 ,font=('times', 10, ' bold ')) 
lbl.place(x=10+x_ch, y=300+y_ch)
txt.place(x=140+x_ch, y=300+y_ch)
lbl2.place(x=10+x_ch, y=350+y_ch)
txt2.place(x=140+x_ch, y=350+y_ch)
message.place(x=140, y=180)
lbl3.place(x=10, y=220)
message2.place(x=10, y=250)
# ------------------------------------------# window-elements-end

# --->bottom layoyt to call functions
clearButton = tk.Button(window, text="Clear", command=clear  ,fg="gray1"   ,bg="snow" ,width=10  ,height=1 ,activebackground = "green2" ,font=('times', 12, ' bold '))
clearButton.place(x=450+x_ch, y=290+y_ch)
clearButton2 = tk.Button(window, text="Clear", command=clear2  ,fg="gray1"   ,bg="snow" ,width=10  ,height=1, activebackground = "green2" ,font=('times', 12, ' bold '))
clearButton2.place(x=450+x_ch, y=340+y_ch)    
takeImg = tk.Button(window, text="Add Student", command=capture  ,fg="gray1"   ,bg="snow"  ,width=12  ,height=1, activebackground = "green2" ,font=('times', 12, ' bold '))
takeImg.place(x=30+x_ch, y=400+y_ch)
trackImg = tk.Button(window, text="Train Model", command=TrainModel  ,fg="gray1"   ,bg="snow"  ,width=12  ,height=1, activebackground = "green2" ,font=('times', 12, ' bold '))
trackImg.place(x=155+x_ch, y=400+y_ch)
rem = tk.Button(window, text="Remove", command=remove  ,fg="gray1"   ,bg="snow"  ,width=12  ,height=1, activebackground = "green2" ,font=('times', 12, ' bold '))
rem.place(x=280+x_ch, y=400+y_ch)
train = tk.Button(window, text="Take Attendance", command=TakeAtten  ,fg="gray1"   ,bg="snow"  ,width=12  ,height=1, activebackground = "green2" ,font=('times', 12, ' bold '))
train.place(x=410+x_ch, y=400+y_ch)
copyWrite = tk.Text(window, background=window.cget("background"), borderwidth=0,font=('times', 15, 'bold'))
copyWrite.tag_configure("superscript", offset=10)
copyWrite.insert("insert", "Project Of Harshit Soni")
copyWrite.configure(state="disabled",fg="gray1"  )
copyWrite.pack(side="right")
copyWrite.place(x=10, y=670)


window.mainloop() #loop for window 