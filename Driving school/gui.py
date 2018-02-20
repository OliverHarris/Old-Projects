import gi #for the userinterface
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import json
import share
class windowDeal():
    def __init__(self,builder,name):
        self.window = builder.get_object(name)
        self.window.connect("destroy",Gtk.main_quit)
    def openWindow(self):#when we want this window we call this
        self.window.show_all()
    def hideWindow(self):
        self.window.hide()#hides it, doesnt destroy

def removeLe(self,ids,builder,window):
    share.removeLess(ids,builder)#remove lesson
    populateLessons(builder,window)#repopulate grid

def removeIns(self,ids,builder,window):
    share.removeIns(ids,builder)#remove instructor
    populateIns(builder,window)#repopulate

def removeCar(self,ids,builder,window):
    share.removeCar(ids,builder)#remove car
    populateCars(builder,window)#repopulate

def removeStu(self,ids,builder,window):
    share.removeLe(ids,builder)#remove student
    populateStu(builder,window)#repopulate

def addLesson(builder,window):
    #This sets up the autocompelete
    insBox = builder.get_object("ins")#instructor
    lerBox = builder.get_object("ler")#learner


    ex = share.getInstructors()
    liststore = Gtk.ListStore(str)
    print ex
    for ids,ins in ex:
        liststore.append([ins])

    ex2 = share.getLearners()
    liststore2 = Gtk.ListStore(str)
    for ids,lear in ex2:
        liststore2.append([lear])
    completion = Gtk.EntryCompletion()
    completion2 = Gtk.EntryCompletion()
    completion2.set_model(liststore2)
    completion2.set_text_column(0)
    completion.set_model(liststore)
    completion.set_text_column(0)

    lerBox.set_completion(completion2)
    insBox.set_completion(completion)

    window.openWindow()




def populateLessons(builder,window):
    try:
        builder.get_object("lessonView").remove(share.grid)
    except:
        pass
    share.grid = Gtk.Grid(column_spacing=20)
    texts = ["Instructor","Learner","Date/time","Length of lesson", "",""]
    for index, item in enumerate(texts):
        la = Gtk.Label("<b>"+item+"</b>")
        la.set_use_markup(True)
        share.grid.attach(la,index,0,1,1)
    ia2 = 0
    for ids,ins,lear,da,leng in share.getLessons():
        share.grid.attach(Gtk.Label(ins),0,ia2+1,1,1)
        share.grid.attach(Gtk.Label(lear),1,ia2+1,1,1)
        share.grid.attach(Gtk.Label(da),2,ia2+1,1,1)
        share.grid.attach(Gtk.Label(leng),3,ia2+1,1,1)
        removeBut = Gtk.Button(label="Remove")
        removeBut.connect("clicked",removeLe,ids,builder,window)
        share.grid.attach(removeBut,4,ia2+1,1,1)
        ia2 +=1
    builder.get_object("lessonView").add(share.grid)
    window.openWindow()



def populateIns(builder,window):
    try:
        builder.get_object("insView").remove(share.grid2)
    except:
        pass
    share.grid2 = Gtk.Grid(column_spacing=20)
    #id   - instructor, dob, car, year, address
    texts = ["Name","DOB","Car","Start year","Address", "Telephone","",""]
    for index, item in enumerate(texts):
        la = Gtk.Label("<b>"+item+"</b>")
        la.set_use_markup(True)
        share.grid2.attach(la,index,0,1,1)
    ia2 = 0
    for ids,ins,dob,car,sy,addr,tel in share.getIns():
        print "ids: ",ids
        share.grid2.attach(Gtk.Label(ins),0,ia2+1,1,1)
        share.grid2.attach(Gtk.Label(dob),1,ia2+1,1,1)
        share.grid2.attach(Gtk.Label(car),2,ia2+1,1,1)
        share.grid2.attach(Gtk.Label(sy),3,ia2+1,1,1)
        share.grid2.attach(Gtk.Label(addr),4,ia2+1,1,1)
        share.grid2.attach(Gtk.Label(tel),5,ia2+1,1,1)
        removeBut = Gtk.Button(label="Remove")
        removeBut.connect("clicked",removeIns,ids,builder,window)
        share.grid2.attach(removeBut,6,ia2+1,1,1)
        ia2 +=1
    builder.get_object("insView").add(share.grid2)
    window.openWindow()


def updateCar(self,spin,ids):
    val = spin.get_value_as_int()
    print val
    share.updateMiles(ids,val)

    populateCars(builder,window)




##The populate functions. Each does the same thing with different information.
#The function uses the share to get the information about learners,lessons, cars etc
#and displays them in the table.
def populateCars(builder,window):
    try:
        builder.get_object("carVie").remove(share.grid3)
    except:
        pass
    share.grid3 = Gtk.Grid(column_spacing=20)
    #id   - instructor, dob, car, year, address
    texts = ["Car","Fuel","Miles","",""]
    for index, item in enumerate(texts):
        la = Gtk.Label("<b>"+item+"</b>")
        la.set_use_markup(True)
        share.grid3.attach(la,index,0,1,1)
    ia2 = 0




    for ids,car,fuel,miles in share.getsCars():
        print "ids: ",ids
        share.grid3.attach(Gtk.Label(car),0,ia2+1,1,1)
        share.grid3.attach(Gtk.Label(fuel),1,ia2+1,1,1)
        #share.grid3.attach(Gtk.Label(miles),2,ia2+1,1,1)
        adjustment = Gtk.Adjustment(miles, 0, 9999999, 10, 100, 0)
        spinbutton = Gtk.SpinButton()
        spinbutton.set_adjustment(adjustment)
        share.grid3.attach(spinbutton,2,ia2+1,1,1)
        removeBut = Gtk.Button(label="Remove")
        removeBut.connect("clicked",removeCar,ids,builder,window)
        updateBut = Gtk.Button(label="Update")
        updateBut.connect("clicked",updateCar,spinbutton,ids)
        share.grid3.attach(removeBut,3,ia2+1,1,1)
        share.grid3.attach(updateBut,4,ia2+1,1,1)
        ia2 +=1
    builder.get_object("carVie").add(share.grid3)
    window.openWindow()



def populateStu(builder,window):
    try:
        builder.get_object("studentView").remove(share.grid4)
    except Exception as e:
        print e
    share.grid4 = Gtk.Grid(column_spacing=20)
    #id   - instructor, dob, car, year, address
    texts = ["Name","Instructor","DOB","Address","Telephone","Email","",""]
    for index, item in enumerate(texts):
        la = Gtk.Label("<b>"+item+"</b>")
        la.set_use_markup(True)
        share.grid4.attach(la,index,0,1,1)
    ia2 = 0


    #id   - name,addr,dob,ins,tel,email


    for ids,name,addr,dob,ins,tel,email in share.getsLea():
        print "ids: ",ids
        share.grid4.attach(Gtk.Label(name),0,ia2+1,1,1)
        share.grid4.attach(Gtk.Label(ins),1,ia2+1,1,1)
        share.grid4.attach(Gtk.Label(addr),2,ia2+1,1,1)
        share.grid4.attach(Gtk.Label(dob),3,ia2+1,1,1)
        share.grid4.attach(Gtk.Label(tel),4,ia2+1,1,1)
        share.grid4.attach(Gtk.Label(email),5,ia2+1,1,1)
        removeBut = Gtk.Button(label="Remove")
        removeBut.connect("clicked",removeStu,ids,builder,window)

        share.grid4.attach(removeBut,6,ia2+1,1,1)

        ia2 +=1
    builder.get_object("studentView").add(share.grid4)
    window.openWindow()
def populateSI(window,builder):
    se = builder.get_object("searchBo").get_text()
    try:
        builder.get_object("searchB").remove(share.sGrid)
    except Exception as e:
        print e
    try:
        builder.get_object("searchB").add(share.gridL2)
    except Exception as e:
        print e


    try:
        d = json.loads(share.getInsDetails(se))
    except:
        share.sGrid = Gtk.Grid(column_spacing=15,row_spacing=30)
        la = Gtk.Label("<b>No details</b>")
        la.set_use_markup(True)
        share.sGrid.attach(la,0,0,1,1)
        builder.get_object("searchB").add(share.sGrid)
        window.openWindow()
        print "not there"
        return

    share.sGrid = Gtk.Grid(column_spacing=15,row_spacing=30)
    la = Gtk.Label("<b>Instructor Name:</b>")
    la.set_use_markup(True)
    share.sGrid.attach(la,0,0,1,1)

    la = Gtk.Label(se)
    la.set_use_markup(True)
    share.sGrid.attach(la,1,0,1,1)


    la1 = Gtk.Label("<b>Address</b>")
    la1.set_use_markup(True)
    share.sGrid.attach(la1,0,1,1,1)

    la = Gtk.Label(d["address"])
    la.set_use_markup(True)
    share.sGrid.attach(la,1,1,1,1)


    la2 = Gtk.Label("<b>DOB</b>")
    la2.set_use_markup(True)
    share.sGrid.attach(la2,0,2,1,1)

    la = Gtk.Label(d["DOB"])
    la.set_use_markup(True)
    share.sGrid.attach(la,1,2,1,1)


    la3 = Gtk.Label("<b>Year of start</b>")
    la3.set_use_markup(True)
    share.sGrid.attach(la3,3,1,1,1)

    la = Gtk.Label(d["year"])
    la.set_use_markup(True)
    share.sGrid.attach(la,4,1,1,1)

    la4 = Gtk.Label("<b>Car</b>")
    la4.set_use_markup(True)
    share.sGrid.attach(la4,3,0,1,1)

    la = Gtk.Label(share.getCar(d["car"]))
    la.set_use_markup(True)
    share.sGrid.attach(la,4,0,1,1)



    la35 = Gtk.Label("<b>Telephone</b>")
    la35.set_use_markup(True)
    share.sGrid.attach(la35,3,2,1,1)

    la8 = Gtk.Label(d["tel"])
    la8.set_use_markup(True)
    share.sGrid.attach(la8,4,2,1,1)


    la5 = Gtk.Label("<b>lessons</b>")
    la5.set_use_markup(True)
    share.sGrid.attach(la5,3,3,1,1)




    ##next lessons set.
    lSet = json.loads(share.getLessonsPerI(d["ids"]))
    #who with , when, how long.

    share.gridL2 = Gtk.Grid(column_spacing=15,row_spacing=5)
    la5 = Gtk.Label("<b>Student</b>")
    la5.set_use_markup(True)
    share.gridL2.attach(la5,0,0,1,1)
    la5 = Gtk.Label("<b>Time/date</b>")
    la5.set_use_markup(True)
    share.gridL2.attach(la5,1,0,1,1)
    la5 = Gtk.Label("<b>Length</b>")
    la5.set_use_markup(True)
    share.gridL2.attach(la5,2,0,1,1)
    ia2 = 0
    for a in lSet["learner"]:
        print a
        share.gridL2.attach(Gtk.Label(a),0,ia2+1,1,1)
        ia2 +=1
    ia2=0
    for a in lSet["d"]:
        print a

        share.gridL2.attach(Gtk.Label(a),1,ia2+1,1,1)
        ia2 +=1
    ia2=0
    for a in lSet["lengthOfLesson"]:
        print a
        share.gridL2.attach(Gtk.Label(a),2,ia2+1,1,1)
        ia2 +=1

    builder.get_object("searchB").add(share.sGrid)
    builder.get_object("searchB").add(share.gridL2)
    window.openWindow()


def populateSL(window,builder):
    se = builder.get_object("searchBo").get_text()
    print se
    try:
        builder.get_object("searchB").remove(share.sGrid)
    except Exception as e:
        print e
    try:
        builder.get_object("searchB").add(share.gridL2)
    except Exception as e:
        print e

    try:
        d = json.loads(share.getLearDetails(se))
    except Exception as e:
        share.sGrid = Gtk.Grid(column_spacing=15,row_spacing=30)
        la = Gtk.Label("<b>No details</b>")
        la.set_use_markup(True)
        share.sGrid.attach(la,0,0,1,1)
        builder.get_object("searchB").add(share.sGrid)
        window.openWindow()
        print "not there"
        print e
        return

    share.sGrid = Gtk.Grid(column_spacing=15,row_spacing=30)
    la = Gtk.Label("<b>Student Name:</b>")
    la.set_use_markup(True)
    share.sGrid.attach(la,0,0,1,1)

    la = Gtk.Label(se)
    la.set_use_markup(True)
    share.sGrid.attach(la,1,0,1,1)


    la1 = Gtk.Label("<b>Address</b>")
    la1.set_use_markup(True)
    share.sGrid.attach(la1,0,1,1,1)

    la = Gtk.Label(d["address"])
    la.set_use_markup(True)
    share.sGrid.attach(la,1,1,1,1)


    la2 = Gtk.Label("<b>DOB</b>")
    la2.set_use_markup(True)
    share.sGrid.attach(la2,0,2,1,1)

    la = Gtk.Label(d["DOB"])
    la.set_use_markup(True)
    share.sGrid.attach(la,1,2,1,1)


    la3 = Gtk.Label("<b>Telephone number</b>")
    la3.set_use_markup(True)
    share.sGrid.attach(la3,3,1,1,1)

    la = Gtk.Label(d["tel"])
    la.set_use_markup(True)
    share.sGrid.attach(la,4,1,1,1)

    la4 = Gtk.Label("<b>Instructor</b>")
    la4.set_use_markup(True)
    share.sGrid.attach(la4,3,0,1,1)

    la = Gtk.Label(share.getCar(d["instructor"]))
    la.set_use_markup(True)
    share.sGrid.attach(la,4,0,1,1)







    la42 = Gtk.Label("<b>Email</b>")
    la42.set_use_markup(True)
    share.sGrid.attach(la42,0,3,1,1)
    la21 = Gtk.Label(d["email"])
    la21.set_use_markup(True)
    share.sGrid.attach(la21,1,3,1,1)





    la43 = Gtk.Label("<b>Total lessons</b>")
    la43.set_use_markup(True)
    share.sGrid.attach(la43,3,3,1,1)

    la211 = Gtk.Label(share.getLessonsNumPerL(d["ids"]))
    la211.set_use_markup(True)
    share.sGrid.attach(la211,4,3,1,1)







    la5 = Gtk.Label("<b>lessons</b>")
    la5.set_use_markup(True)
    share.sGrid.attach(la5,3,4,1,1)




    ##next lessons set.
    lSet = json.loads(share.getLessonsPerL(d["ids"]))

    #who with , when, how long.

    share.gridL2 = Gtk.Grid(column_spacing=15,row_spacing=5)
    la5 = Gtk.Label("<b>Student</b>")
    la5.set_use_markup(True)
    share.gridL2.attach(la5,0,0,1,1)
    la5 = Gtk.Label("<b>Time/date</b>")
    la5.set_use_markup(True)
    share.gridL2.attach(la5,1,0,1,1)
    la5 = Gtk.Label("<b>Length</b>")
    la5.set_use_markup(True)
    share.gridL2.attach(la5,2,0,1,1)
    ia2 = 0
    for a in lSet["learner"]:
        print a
        share.gridL2.attach(Gtk.Label(a),0,ia2+1,1,1)
        ia2 +=1
    ia2=0
    for a in lSet["d"]:
        print a
        share.gridL2.attach(Gtk.Label(a),1,ia2+1,1,1)
        ia2 +=1
    ia2=0
    for a in lSet["lengthOfLesson"]:
        print a
        share.gridL2.attach(Gtk.Label(a),2,ia2+1,1,1)
        ia2 +=1

    builder.get_object("searchB").add(share.sGrid)
    builder.get_object("searchB").add(share.gridL2)
    window.openWindow()

def showAddStu(builder,window):

    cIns = builder.get_object("sIns")


    ex = share.getInstructors()
    liststore = Gtk.ListStore(int,str)
    print ex
    for ids,ins in ex:
        liststore.append([int(ids),ins])
    cIns.set_model(liststore)
    cell = Gtk.CellRendererText()
    cIns.pack_start(cell, True)
    cIns.add_attribute(cell, 'text', 1)
    #cIns.set_entry_text_column(1)

    window.openWindow()



def addIns(builder,window):
    #sets up autocompelete
    name_store = Gtk.ListStore(int, str)
    for car in share.getCars():
        name_store.append([int(car[0]),car[1]])
    vbox = builder.get_object("iCar")
    vbox.set_model(name_store)
    cell = Gtk.CellRendererText()
    vbox.pack_start(cell, True)
    vbox.add_attribute(cell, 'text',1)
    window.openWindow()
