from flask import Flask, render_template, request,redirect,session, url_for
import os 
import pandas as pd
import csv

import sqlite3 as sql

import PyPDF2
import re

app = Flask(__name__)


app.config['SECRET_KEY'] = 'super secret key'

UPLOAD_FOLDER = 'C:/Users/mamats/Desktop/work/Medical1/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#base code
@app.route('/')
def index():
   return render_template('home.html')


@app.route('/gallery')
def gallery():
    return render_template("gallery.html")


@app.route("/signup", methods = ["GET","POST"])
def signup():
    msg=None
    if(request.method=="POST"):
        if (request.form["uname"]!="" and request.form["uphone"]!="" and request.form["username"]!="" and request.form["upassword"]!=""):
            username=request.form["username"]
            password=request.form["upassword"]
            uname=request.form["uname"]
            uphone=request.form["uphone"]


            with sql.connect("hospital.db") as con:
                c=con.cursor()
                c.execute("INSERT INTO  signup VALUES('"+uname+"','"+uphone+"','"+username+"','"+password+"')")
                msg = "Your account is created"

                con.commit()
        else:
            msg="Something went wrong"


    return render_template("signup.html", msg=msg)

@app.route('/user')
def user():
    return render_template("userlogin.html")

@app.route('/userloginNext',methods=['GET','POST'])
def userloginNext():
    msg=None
    if (request.method == "POST"):
        username = request.form['username']
      
        upassword = request.form['upassword']
        
        with sql.connect("hospital.db") as con:
            c=con.cursor()
            c.execute("SELECT username,upassword  FROM signup WHERE username = '"+username+"' and upassword ='"+upassword+"'")
            r=c.fetchall()
            for i in r:
                if(username==i[0] and upassword==i[1]):
                    session["logedin"]=True
                    session["username"]=username
                    return redirect(url_for("userhome"))
                else:
                    msg= "please enter valid username and password"
                    return render_template("userlogin.html",msg=msg)
    
    return render_template("userlogin.html",msg=msg)


#usercode

@app.route('/userhome')
def userhome():
    return render_template("userhome.html")


@app.route('/uploadfile')
def uploadfile():
    return render_template("useruploadfile.html")



@app.route('/userlogout')
def userlogout():
	# Remove the session variable if present
	session.clear()
	return redirect(url_for('index'))

rx_dict = {
   

    'name': re.compile(r'Name: (?P<name>[a-zA-Z]+\. [a-zA-Z]+ )'),
    'age': re.compile(r'(.*)Age/Sex: (?P<age>[0-9]+ )'),
    'date':re.compile(r'(.*)Admission Date: (?P<date>[0-9]+ - [0-9]+ - [0-9]+ [0-9]+:[0-9]+)'),
    'd_date':re.compile(r'(.*)Discharge Date: (?P<d_date>[0-9]+ - [0-9]+ - [0-9]+ [0-9]+:[0-9]+)'),
    
    'desease':re.compile(r'Disease: (?P<desease>[a-zA-Z]+ [a-zA-Z]+)'),
   
    #'location':re.compile(r'(.*)Location: (?P<location>[a-zA-Z]+, [a-zA-Z]+)')
    'location':re.compile(r'(.*)Location: (?P<location>[a-zA-Z]+, [a-zA-Z]+)'),
    'zipcode': re.compile(r'(.*)Zipcode: (?P<zipcode>[0-9]+)'),
    'gender':re.compile(r'(.*)Y/(?P<gender>[a-zA-Z]+)')

}

def parse_line(line):
   for key,rx in rx_dict.items():
      match = re.search(rx,line)
      if match:
         return key,match

   return None,None


def FinalCode():
   
   #filepath = 'Delete/output_final.txt'
   with open('Delete/output_final.txt','r') as f:
      line=f.readline()
      while line:
         key,match=parse_line(line)
         if key=='name': 
            name=match.group('name')
            

         elif key=='age':
            age=match.group('age')
            

         elif key=='date':
            date=match.group('date')
          

         elif key=='d_date':
            d_date=match.group('d_date')
         
         elif key=='zipcode':
            zipcode=match.group('zipcode')
            

         elif key=='desease':
            desease=match.group('desease')
            

         elif key=='location':
            location=match.group('location')
         
         elif key=='gender':
            gender=match.group('gender')
               
          
            
         line=f.readline()
  
   return name,age,date,d_date,zipcode,desease,location,gender    
   

def NoiseRemoval():
   with open('Delete/output.txt') as f:
      all_lines = f.readlines()
      all_lines = [x.strip() for x in all_lines if x.strip()]
      PName = " ".join(x for x in all_lines[:3])
      PAge= " ".join(x for x in all_lines[4:7])

      PAdmissionDt=" ".join(x for x in all_lines[8:15])
      PDischargeDt=" ".join(x for x in all_lines[14:23])
   
      PDesease=" ".join(x for x in all_lines[28:33])
      PLocation=" ".join(x for x in all_lines[20:26])
      PTreatment=" ".join(x for x in all_lines[99:167])
      zipcode=" ".join(x for x in all_lines[25:28])
      Pgender=" ".join(x for x in all_lines[5:7])
      with open("Delete/output_final.txt",'w') as f1:
         f1.write(PName)
         f1.write('\n')
         f1.write(PAge)
         f1.write('\n')
         f1.write(PAdmissionDt)
         f1.write('\n')
         f1.write(PDischargeDt)
         f1.write('\n')
         f1.write(PDesease)
         f1.write('\n')
         f1.write(PLocation)
         f1.write('\n')
         f1.write(PTreatment)
         f1.write('\n')
         f1.write(zipcode)
         f1.write('\n')
         f1.write(Pgender)
      f1.close()
   

def convert(f):
   pdfread = PyPDF2.PdfFileReader(f)
   i=0
   while i<pdfread.getNumPages():
      pageinfo = pdfread.getPage(i)
   # print(pageinfo.extractText())
      pdfdata=pageinfo.extractText()
      with open("Delete/Dischargdraftt.txt","a",encoding='utf-8') as f1:
         f1.write(pdfdata)
      i = i+1  
def Rawtextconverter():
   fh = open("Delete/Dischargdraftt.txt", "r")
   lines = fh.readlines()
   fh.close()

   keep = []
   for line in lines:
      if not line.isspace():
         lin=re.sub(' +',' ',line)
         keep.append(lin)

   fh = open("Delete/output.txt", "w")
   fh.write("".join(keep))
# should also work instead of joining the list:
# fh.writ elines(keep)
   fh.close()

@app.route('/clear', methods= ['POST'])
def clear():
   dir = 'Delete/'
   for f in os.listdir(dir):
      os.remove(os.path.join(dir, f))
   return render_template('useruploadfile.html')

@app.route('/success', methods = ['POST'])  
def success():  
   if request.method == 'POST':  
      f = request.files['file']  
        #f.save(f.filename)  
      f.save(os.path.join(app.config['UPLOAD_FOLDER'], f.filename))
      
       
      convert(f)
      Rawtextconverter()
      NoiseRemoval()
      try:
         name1,age,date1,d_date,zipcode,desease,location,gender = FinalCode()
      except UnboundLocalError: 
         return render_template('useruploadfile.html',msg="Model will not able to predict as it is not valid PDF format")
      


      #data=createdate_frame(name1,age,date,d_date,doctor,location)
      #print(data)

      with sql.connect("hospital.db") as con:
        c=con.cursor()
        c.execute("INSERT INTO predict (uname,uage,ugender,udate,uddate,udesease,ulocation,uzipcode) values(?,?,?,?,?,?,?,?)",(name1,age,gender,date1,d_date,desease,location,zipcode)) 
        con.commit()

     # with open('datastore.csv', 'a', newline='') as file:
      #   writer = csv.writer(file)
      #   writer.writerow([name1,age,date1,d_date,doctor,location ])
      
      
      #return render_template('viewresult.html', df_view=df)
      return render_template('useruploadfile.html',name2="Patient Name: "+name1,age2="Age: "+age,gender="Gender: "+gender,date2="Admission Date: "+date1,d_date2="Discharge Date: "+d_date,desease="Desease: "+desease,location2="Location: "+location,zipcode="Zipcode: "+zipcode)

@app.route('/viewresult')
def viewresult():
    con=sql.connect("hospital.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("select * from predict")
    rows=cur.fetchall()
    print(rows)
    
    return render_template("viewrecord.html",rows=rows)
      
if __name__ == '__main__':
   app.run(debug = True)