import gi #for the userinterface
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import gui,share #my other py files

window = {}#login,error,main - windows.


class Handler:
    def onDeleteWindow(self, *args):#When the main window is blocked it calls this handler (function)
        Gtk.main_quit()
    def tryLogin(self,*args):
        username = builder.get_object("username").get_text()#get the username
        password = builder.get_object("password").get_text()#get the password
        builder.get_object("password").set_text("")#clear the password entry
        if(share.checkLogin(username,password)):#check if the login is correct
            window["login"].hideWindow()#from the gui file these functions are called
            window["main"].openWindow()
        else:
            window["error"].openWindow()
    def openStudents(*args):
        window["students"].openWindow()
        gui.populateStu(builder,window["students"])#from the gui function the populate students is called
    def addCar(*args):
        share.addCar(builder)#In the share file this adds a car to the database
        gui.populateCars(builder,window["car"])#Update the window with the new information

    def hideMe(self,win,*args):#As these windows need to be opened again we can just hide them
        try:
            builder.get_object("lessonView").remove(share.grid)#restarts the lessons table.
        except:
            pass
        try:
            builder.get_object("insView").remove(share.grid2)#restarts any grids that may cause duplication
        except:
            pass
        win.hide()
        return True
    def logout(self,win,*args):
        for a,b in window.iteritems():
            b.hideWindow()#close all the windows
        window["login"].openWindow()
        pass
    def showAddIns(self,*args):
        gui.addIns(builder,window["addIns"])#add instructor
    def openSearch(*args):
        ex = share.getInstructors()
        liststore = Gtk.ListStore(str)
        print ex
        for ids,ins in ex:
            liststore.append([ins])#add the instrcutor to the liststore


        for s in share.getLearners():
            liststore.append([s[1]])
        completion = Gtk.EntryCompletion()
        completion.set_model(liststore)
        completion.set_text_column(0)
        builder.get_object("searchBo").set_completion(completion)#builder gets the object from the glade file (Xml)
        window["search"].openWindow()
    def oStudents(*args):
        gui.showAddStu(builder,window["addS"])#Show the add students window
    def doCalss(*args):
        print "calculations"#<--
        share.doCal()
        doneWin = Gtk.Window()
        done = Gtk.Label("<b>Finished calculations</b>")
        done.set_use_markup(True)
        doneWin.add(done)
        doneWin.connect("delete-event", closeDone)
        doneWin.show_all()
    def instr(*args):
        window["instructors"].openWindow()
        gui.populateIns(builder,window["instructors"])
        print "finished ins"
    def searchIns(*args):#search instructor
        grid = builder.get_object("searchB")
        i = 0
        for child in grid.get_children():
            if (i<2):#Don't remove the first two elements of the grid.
                i +=1
                print "pass"
                continue
            print child

            grid.remove(child)


        gui.populateSI(window["search"],builder)

    def searchLe(*args):#Search learner
        grid = builder.get_object("searchB")
        i = 0
        for child in grid.get_children():
            if (i<2):
                i +=1
                print "pass"
                continue
            print child

            grid.remove(child)

        gui.populateSL(window["search"],builder)
    def openAddLessons(*args):
        gui.addLesson(builder,window["addLesson"])
    def closeError(self,*args):
        window["error"].hideWindow()
    def hideThis(self,a,*args):
        a.hide()
        return True
    def carAdd(*args):
        window["addCar"].openWindow()
    def addIns(*args):
        share.newIns(builder)#New instructor to the database
        gui.populateIns(builder,window["instructors"])

    def dispCars(*args):
        gui.populateCars(builder,window["car"])
    def lessons(self,*args):
        window["lessons"].openWindow()
        gui.populateLessons(builder,window["lessons"])

    def makeLe(*args):
        share.newLesson(builder)
        gui.populateLessons(builder,window["lessons"])
    def addS(*args):
        share.newStudent(builder)
        gui.populateStu(builder,window["students"])
def closeDone(a,b,*args):
    a.hide()

builder = Gtk.Builder()#What makes our gui file
builder.add_from_file("design.glade")#the layout
builder.connect_signals(Handler())#connects the handlers to the class
window["login"] = gui.windowDeal(builder,"loginWindow")#gets each window from the layout
window["error"] = gui.windowDeal(builder,"errorLogin")
window["main"] = gui.windowDeal(builder,"mainWindow")
window["car"] = gui.windowDeal(builder,"carView")
window["addLesson"] = gui.windowDeal(builder,"addWindow")
window["addCar"] = gui.windowDeal(builder,"addCar")
window["addIns"] = gui.windowDeal(builder,"addIns")
window["lessons"] = gui.windowDeal(builder,"lessonWindow")
window["students"] = gui.windowDeal(builder,"studentsWindow")
window["instructors"] = gui.windowDeal(builder,"instructorView")
window["addS"] = gui.windowDeal(builder,"addStu")
window["search"] = gui.windowDeal(builder,"searchBox")

window["login"].openWindow()
Gtk.main()#main loop for the gui
