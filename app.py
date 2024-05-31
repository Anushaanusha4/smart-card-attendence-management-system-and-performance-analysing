from flask import Flask, render_template, request
import os
import pandas as pd
import datetime
import time
import cv2
import csv
import geocoder
import telepot

app = Flask(__name__)

def getid():
   if not os.path.exists('StudentDetails.csv'):
      return 1
   else:
      df = pd.read_csv('StudentDetails.csv')
      names1 = df['Id'].values
      names1 = list(set(names1))
      return int(names1[-1])+1

@app.route('/')
def index():
   return render_template("index.html", id=getid())

@app.route('/create_datsets',  methods=['POST','GET'])
def create_datsets():
   if request.method == 'POST':
      Id = request.form['Id']
      Name = request.form['Name']
      usn = request.form['usn']
      Phone = request.form['Phone']
      Email = request.form['Email']
      Sem = request.form['Sem']
      Cource = request.form['Cource']
      Branch = request.form['Branch']
      cardnum = request.form['cardnum']

      print(Id+' '+Name+' '+usn+' '+Phone+' '+Email+' '+Sem+' '+Cource+' '+Branch+' '+cardnum)

      msg = ['Images Saved for',
            'ID : ' + Id,
            'USN : ' + usn,
            'Name : ' + Name,
            'Phone : ' + Phone,
            'Email : ' + Email,
            'Semester : ' + Sem,
            'Cource : ' + Cource,
            'Branch : ' + Branch,
            'Card No : ' + cardnum]
      
      row = [Id, usn, Name, Phone, Email, Sem, Cource, Branch, cardnum]

      if not os.path.exists('StudentDetails.csv'):
         row1 = ['Id','USN', 'Name', 'Phone', 'Email', 'Sem', 'Cource', 'Branch', 'cardnum']
         with open('StudentDetails.csv','w',newline='') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row1)
         csvFile.close()

      with open('StudentDetails.csv','a', newline='') as csvFile:
         writer = csv.writer(csvFile)
         writer.writerow(row)
      csvFile.close()

      return render_template("index.html", msg=msg, id=getid())
   return render_template("index.html", id=getid())

@app.route('/attendence',  methods=['POST','GET'])
def attendence():
   if request.method == 'POST':
      Subject = request.form['Subject']
      
      location = geocoder.ip('me')
      langitude = location.latlng[0]
      lattitude = location.latlng[1]
                         
      from serial_test import read_data
      data = read_data()
      List = []
      names = []
      f = open('StudentDetails.csv', 'r')
      reader = csv.reader(f)
      for row in reader:
         names.append(row[1])
      f.close()
      ts = time.time()      
      date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
      timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
      Hour,Minute,Second=timeStamp.split(":")
      fileName="StudentAttendence/"+str(Subject)+"/Attendence_"+date+"_"+Hour+"-"+Minute+"-"+Second+".csv"
      for d in data:
         status = None
         f = open('StudentDetails.csv', 'r')
         reader = csv.reader(f)
         for row in reader:
            print(row)
            if d in row:
               print('ppppppppp')
               status = row
               break

         if status: 
            f = open(fileName, 'a')
            writer = csv.writer(f)
            writer.writerow(['Id', 'Name', 'Phone', 'Email', 'Sem', 'Cource', 'Branch', 'cardnum'])
            writer.writerow(status)
            f.close()
            List.append(status[1])
         else:
            print('Invalid card')

      present_list = []
      absense_list = []
      print(List)
      print(names)
      for name in names[1:]:
         if name in List:
            print('presence')
            present_list.append(name)
            bot = telepot.Bot('7009632554:AAHoqROOslY4WdFtzotEt-vlgmMed94JR5M')
            bot.sendMessage('6491725070', str(f'{name} is present on {date} at {timeStamp}'))
            bot = telepot.Bot('7091463032:AAEGXym0S2PcvvX7oZ3ZbINOFgkF6EMk_KQ')
            bot.sendMessage('1657252828', str(f'{name} is present on {date} at {timeStamp}'))
         else:
            print('absence')
            absense_list.append(name)
            bot = telepot.Bot('7009632554:AAHoqROOslY4WdFtzotEt-vlgmMed94JR5M')
            bot.sendMessage('6491725070', str(f'{name} is absent on {date} at {timeStamp}'))
            bot = telepot.Bot('7091463032:AAEGXym0S2PcvvX7oZ3ZbINOFgkF6EMk_KQ')
            bot.sendMessage('1657252828', str(f'{name} is absent on {date} at {timeStamp}'))

      return render_template("index.html", Subject=Subject, Date=date, Time=timeStamp, id=getid(), present_list=present_list, absense_list=absense_list)

   return render_template("index.html", id=getid())

@app.route('/library')
def library():
   return render_template("library.html")
   
@app.route('/Take',  methods=['POST','GET'])
def Take():
   if request.method == 'POST':
      from serial_test import read_data1
      data = read_data1()
      df=pd.read_csv("StudentDetails.csv")
      Cardnum=df.loc[df['cardnum'] == data]
      print(Cardnum)
      if Cardnum.empty:
         return render_template("library.html", msg="Invalid card")
      else:
         df.to_csv("StudentDetails.csv", index=False)
         book = request.form['book']
         if not os.path.exists(book+'.csv'):
            f = open(book+'.csv', 'w')
            writer = csv.writer(f)
            writer.writerow(['cardnum', 'Take', 'Ldate'])
            f.close()

         from datetime import date, timedelta
         date_1 = date.today()
         end_date = date_1 + timedelta(days=5)
         end_date= str(end_date)

         f = open(book+'.csv', 'a')
         writer = csv.writer(f)
         writer.writerow([data, date_1, end_date])
         f.close()

         msg = "{} book taken by {} ({}) on {} and last date to return on {}".format(book, Cardnum['Name'].values[0], data, date_1, end_date)

         bot = telepot.Bot('7009632554:AAHoqROOslY4WdFtzotEt-vlgmMed94JR5M')
         bot.sendMessage('6491725070', str(msg))
         bot = telepot.Bot('7091463032:AAEGXym0S2PcvvX7oZ3ZbINOFgkF6EMk_KQ')
         bot.sendMessage('1657252828', str(msg))

         return render_template("library.html", msg=msg)
   return render_template("library.html")

@app.route('/Return',  methods=['POST','GET'])
def Return():
   if request.method == 'POST':
      from serial_test import read_data1
      data = read_data1()
      df=pd.read_csv("StudentDetails.csv")
      Cardnum=df.loc[df['cardnum'] == data]
      if Cardnum.empty:
         return render_template("library.html", msg="Invalid card")
      else:
         df.to_csv("StudentDetails.csv", index=False)
         book = request.form['book']

         from datetime import date
         date_1 = date.today()
         date_1= str(date_1)

         df=pd.read_csv(book+".csv")
         ev=df.loc[(df['cardnum']==str(data)),'Return']=date_1
         df.to_csv(book+".csv", index=False)

         msg = "{} book returned by {} on {}".format(book, data, date_1)

         bot = telepot.Bot('7009632554:AAHoqROOslY4WdFtzotEt-vlgmMed94JR5M')
         bot.sendMessage('6491725070', str(msg))
         bot = telepot.Bot('7091463032:AAEGXym0S2PcvvX7oZ3ZbINOFgkF6EMk_KQ')
         bot.sendMessage('1657252828', str(msg))

         return render_template("library.html", msg=msg)
   return render_template("library.html")


@app.route('/getDetails',  methods=['POST','GET'])
def getDetails():
   if request.method == 'POST':
      file = request.form['sem']
      from serial_test import read_data1
      data = read_data1()
      df=pd.read_csv("StudentDetails.csv")
      USN=str(df.loc[df['cardnum'] == data, 'USN'].values[0])
      print(USN)

      f = open(file+".csv", 'r')
      reader = csv.reader(f)
      rows = None
      header = next(reader)
      for row in reader:
         if USN in row:
            rows = row
            break
      if rows:
         print(rows)
      f.close()

      fileName = None
      for file in os.listdir('static/marks'):
         if data in file:
            fileName = file
      
      f = open("fees.csv", 'r')
      reader = csv.reader(f)
      fees = None
      header1 = next(reader)
      for row in reader:
         if USN in row:
            fees = row
            break
      print(fees)
      return render_template("details.html",row = rows, fileName=fileName, header=header, header1=header1, fees=fees)
   return render_template("details.html")

@app.route('/student_details', methods=['POST', 'GET'])
def student_details():
   return render_template('details.html')

if __name__ == "__main__":
   app.run(debug=True, use_reloader=False)
