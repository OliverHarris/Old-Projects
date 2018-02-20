import sqlite3 as lite#database
import json,time
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
global grid,grid2,grid3,grid4,sGrid,gridL2
con = lite.connect("data.db")#connect to the database file
with con:
    cur = con.cursor()#sets up the connection with the database
def checkLogin(username,password):
    cur.execute("SELECT * FROM login WHERE username=? AND password=?",(username,password,))
    row =cur.fetchone()#should only find one
    if(row == None):#No login found, incorrect username or password
        return False
    else:
        return True#Correct login!
def removeLess(number,builder):
    print number
    with con:
        cur2 = con.cursor()
        cur2.execute("DELETE FROM lessons WHERE lessonId=? ",(number,))#remove the lesson from the database where the ID matches

    #builder.get_object("lessonView").remove(grid)

def getLessonsPerI(i):#lessons per instructor
    con = lite.connect("data.db")
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM lessons where instructor=?",(i,))
        rows =cur.fetchall()

        ids=[]
        ins=[]
        le=[]
        d=[]
        leng=[]
        for r in rows:
            ids.append(str(r[0]))
            ins.append(getTeacher(str(r[1])))
            le.append(getLearner(str(r[2])))
            d.append(str(r[3]))
            leng.append(r[4])
        j = json.dumps({"ids":ids,"instructor":ins,"learner":le,"d":d,"lengthOfLesson":leng})#For this we use JSON to format the data

        return j
def getLessonsNumPerL(i):#lessons per learner
    con = lite.connect("data.db")
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM lessons where learner=?",(i,))
        rows =cur.fetchall()
        tot = 0
        for r in rows:
            tot +=1

        return str(tot)



def getInsDetails(name):#instructor details
    con = lite.connect("data.db")
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM instructors where instructorName=?",(name,))
        r = cur.fetchone()
        j = json.dumps({"ids":r[0],"instructor":r[1],"DOB":r[2],"car":r[3],"year":r[4],"address":r[5],"tel":r[6]})

        return j
def getLearDetails(name):#learner details
    con = lite.connect("data.db")
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM learners where studentName=?",(name,))
        r = cur.fetchone()
        j = json.dumps({"ids":r[0],"address":r[2],"DOB":r[3],"instructor":r[4],"tel":r[5],"email":r[6]})

        return j

def getLessonsPerL(i):#lessons information
    con = lite.connect("data.db")
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM lessons where learner=?",(i,))
        rows =cur.fetchall()

        ids=[]
        ins=[]
        le=[]
        d=[]
        leng=[]
        for r in rows:
            ids.append(str(r[0]))
            ins.append(getTeacher(str(r[1])))
            le.append(getLearner(str(r[2])))
            d.append(str(r[3]))
            leng.append(r[4])
        j = json.dumps({"ids":ids,"instructor":ins,"learner":le,"d":d,"lengthOfLesson":leng})

        return j


def removeLe(number,builder):
    print number
    with con:
        cur2 = con.cursor()
        cur2.execute("DELETE FROM learners WHERE learnerId=? ",(number,))#delete learner where it matches learnerid

    #builder.get_object("studentView").remove(grid4)

def removeIns(number,builder):
    print number
    with con:
        cur2 = con.cursor()
        cur2.execute("DELETE FROM instructors WHERE instructorId=? ",(number,))#remove instructor where it matches the instructorid

    builder.get_object("insView").remove(grid2)

def updateMiles(ids,miles):
    with con:
        cur2 = con.cursor()
        cur2.execute("UPDATE cars SET miles=? WHERE carId=? ",(miles,ids))#UPDATE the miles where it matches the carid

def removeCar(number,builder):
    print number
    with con:
        cur2 = con.cursor()
        cur2.execute("DELETE FROM cars WHERE carId=? ",(number,))

    builder.get_object("carVie").remove(grid3)

def getIdLer(ler):
    cur.execute("SELECT * FROM learners WHERE studentName=?",(ler,))
    return cur.fetchone()[0]
def getIdIns(ins):

    cur.execute("SELECT * FROM instructors WHERE instructorName=?",(ins,))
    return cur.fetchone()[0]

def getInstructors():
    con = lite.connect("data.db")
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM instructors")
        r = cur.fetchall()
        for i in r:

            print i[0],i[1]
            yield str(i[0]),i[1]
            #id, name
def newLesson(builder):
    ins =builder.get_object("ins").get_text()
    lear = builder.get_object("ler").get_text()
    dt = builder.get_object("date").get_text()
    con = lite.connect("data.db")
    if(ins=="" or lear=="" or dt ==""): #presence check
        print "name is blank"
        messagedialog = Gtk.MessageDialog(parent=None,
                                          flags=Gtk.DialogFlags.MODAL,
                                          type=Gtk.MessageType.ERROR,
                                          buttons=Gtk.ButtonsType.OK,
                                          message_format="Values are incomplete.")

        messagedialog.run()

        messagedialog.destroy()
        return

    ins = getIdIns(ins)
    lear = getIdLer(lear)
    print ins,lear
    with con:
        cur = con.cursor()
        cur.execute("INSERT INTO lessons(lessonId,instructor,learner,dateTime,lengthOfLesson) VALUES(NULL,?,?,?,2)",(ins,lear,dt))

def addCar(builder):
    name =builder.get_object("cName").get_text()
    miles = builder.get_object("cMiles")
    miles = miles.get_value_as_int()
    print "miles: ",miles
    fuel = builder.get_object("cFuel").get_text()
    con = lite.connect("data.db")
    if(name=="" or miles=="" ): #presence check and for the telephone length check
        print "name is blank"
        messagedialog = Gtk.MessageDialog(parent=None,
                                          flags=Gtk.DialogFlags.MODAL,
                                          type=Gtk.MessageType.ERROR,
                                          buttons=Gtk.ButtonsType.OK,
                                          message_format="Values are incomplete.")

        messagedialog.run()

        messagedialog.destroy()
        return

    with con:
        cur = con.cursor()
        cur.execute("INSERT INTO cars(carId,car,fuel,miles) VALUES(NULL,?,?,?)",(name,fuel,miles))


def newIns(builder):
    combo = builder.get_object("iCar")

    index = combo.get_active()
    model = combo.get_model()
    item = model[index]
    print item[0] , item[1]
    car = item[0]
    name=builder.get_object("iName").get_text()


    tel=builder.get_object("iTel").get_text()
    dob=builder.get_object("iDOB").get_text()

    yr=builder.get_object("iYr").get_text()
    addr=builder.get_object("iAddr").get_text()

    if(name=="" or tel=="" or dob =="" or yr== "" or addr=="" or len(tel)!=11): #presence check and for the telephone length check
        print "name is blank"
        messagedialog = Gtk.MessageDialog(parent=None,
                                          flags=Gtk.DialogFlags.MODAL,
                                          type=Gtk.MessageType.ERROR,
                                          buttons=Gtk.ButtonsType.OK,
                                          message_format="Values are incomplete.")

        messagedialog.run()

        messagedialog.destroy()
        return

    con = lite.connect("data.db")

    with con:
        cur = con.cursor()
        cur.execute("INSERT INTO instructors(instructorId,instructorName,instructorDOB,instructorCar,yearOfStart,address,tel)\
         VALUES(NULL,?,?,?,?,?,?)",(name,dob,car,yr,addr,tel))

def newStudent(builder):
    cAddr = builder.get_object("sAddr").get_text()
    cDOB= builder.get_object("sDOB").get_text()
    cName = builder.get_object("sName").get_text()
    cEmail = builder.get_object("sEmail").get_text()
    cIns = builder.get_object("sIns")
    cTel = builder.get_object("sTel").get_text()

    combo = builder.get_object("sIns")
    index = combo.get_active()
    model = combo.get_model()
    item = model[index]
    print item[0] , item[1]
    ins = item[0]

    if(cAddr=="" or cDOB=="" or cName =="" or cEmail== "" or cIns=="" or len(cTel)!=11): #presence check and for the telephone length check
        print "name is blank"
        messagedialog = Gtk.MessageDialog(parent=None,
                                          flags=Gtk.DialogFlags.MODAL,
                                          type=Gtk.MessageType.ERROR,
                                          buttons=Gtk.ButtonsType.OK,
                                          message_format="Values are incomplete.")

        messagedialog.run()

        messagedialog.destroy()
        return


    con = lite.connect("data.db")

    with con:
        cur = con.cursor()
        cur.execute("INSERT INTO learners(learnerId,studentName,studentAddress,studentDOB,instructor,tel,email)\
         VALUES(NULL,?,?,?,?,?,?)",(cName,cAddr,cDOB,ins,cTel,cEmail,))


def getLearners():
    con = lite.connect("data.db")
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM learners")
        r = cur.fetchall()
        for i in r:
            yield i[0],i[1]
            #id, name

def doCal():
    for l in getLearners():
        print l[0]
        con = lite.connect("data.db")
        lessons = []
        st=l[1]
        total = 0
        with con:
            cur = con.cursor()
            cur.execute("SELECT * FROM lessons WHERE learner=?",(l[0],))
            rows = cur.fetchall()
            for r in rows:
                lessons.append("Lesson on the "+str(r[3])+" with "+getTeacher(r[1])+" for "+str(r[4])+" hours.")
                total += r[4]
        print lessons
        print total
        tOutput = "Hello %s. Here are your lessons.\n"% st
        for le in lessons:
            tOutput += le+"\n"
        tOutput+="The total number of hours is "+str(total)
        bill = total*20.54
        pound = u'\u00A3'
        tOutput+="\nCurrently it is 20.54 per hour. Your total bill is "+ str(bill) +" pounds"
        print "*************************"
        f = open("cal/"+st+":"+time.asctime(time.localtime(time.time())),"w")
        f.write(tOutput)
        print tOutput
        print "*************************\n\n\n\n"





def getTeacher(t):
    con = lite.connect("data.db")
    print t
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM instructors where instructorId=?",(t,))
        r = cur.fetchone()
        print r
        return r[1]




def getInstructor(t):
    cur.execute("SELECT * FROM instructors where instructorId=?",(t,))
    r = cur.fetchone()
    return r[1]

def getCar(t):
    cur.execute("SELECT * FROM cars where carId=?",(t,))
    r = cur.fetchone()
    return r[1]

def getLearner(t):
    cur.execute("SELECT * FROM learners where learnerId=?",(t,))
    r = cur.fetchone()
    return r[1]


def getLessons():
    cur.execute("SELECT * FROM lessons")
    rows =cur.fetchall()
    for r in rows:
        yield str(r[0]),getInstructor(str(r[1])),getLearner(str(r[2])),str(r[3]),str(r[4])
        #id   - instructorid, learnerid, datetime, lengthof lessons
def getIns():
    cur.execute("SELECT * FROM instructors")
    rows =cur.fetchall()
    for r in rows:
        yield str(r[0]),str(r[1]),str(r[2]),getCar(r[3]),str(r[4]),str(r[5]),r[6]
        #id   - instructor, dob, car, year, address

def getsCars():
    cur.execute("SELECT * FROM cars")
    rows =cur.fetchall()
    for r in rows:
        yield str(r[0]),str(r[1]),str(r[2]),r[3]
        #id   - car, fuel, car, miles
def getsLea():
    cur.execute("SELECT * FROM learners")
    rows =cur.fetchall()
    for r in rows:
        yield str(r[0]),str(r[1]),str(r[2]),str(r[3]),getInstructor(str(r[4])),str(r[5]),str(r[6])
        #id   - name,addr,dob,ins,tel,email



def getCars():
    cur.execute("SELECT * FROM cars")
    rows =cur.fetchall()
    for r in rows:
        yield str(r[0]),str(r[1])
        #id   - car
