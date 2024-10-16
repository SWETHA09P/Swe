import datetime
from tkinter import *
import mysql.connector
from tkinter import messagebox
mydb = mysql.connector.connect(host="bivpmn8lmtfrb2ckizfa-mysql.services.clever-cloud.com",
                                user="ul7kjuw51idmwufn",
                                passwd="Y59vGTRrnEQaepWvTFQt",
                               database="bivpmn8lmtfrb2ckizfa")
mycursor = mydb.cursor()
def addMov():
    mov = Tk()
    def goBack():
        mov.destroy()
        Admin()
    Button(text="Back", command=goBack).pack()
    mov.title("Admin")
    frame = LabelFrame(mov, padx=100,pady=100 )
    frame.pack()
    e1 = Entry(frame,width=35,borderwidth=5)
    e1.grid(row = 2,column=3,columnspan=3,padx=10,pady=15)
    e1.insert(0,"Name")
    e2 = Entry(frame,width=35,borderwidth=5)
    e2.grid(row = 3,column=3,columnspan=3,padx=10,pady=15)
    e2.insert(0,"language")
    e3 = Entry(frame,width=35,borderwidth=5)
    e3.grid(row = 4,column=3,columnspan=3,padx=10,pady=15)
    e3.insert(0,"genre")
    e4 = Entry(frame,width=35,borderwidth=5)
    e4.grid(row = 5,column=3,columnspan=3,padx=10,pady=15)
    e4.insert(0,"length")
    Label(text="Enter length in HH:MM:SS format").pack()
    def callchk1():
        name = e1.get()
        language = e2.get()
        genre = e3.get()
        length = e4.get()
        mycursor.execute('''insert into movie(name,language,genre,length) values(%s,%s,%s,%s)''',(name,language,genre,length))
        mydb.commit()
        mov.destroy()
    add = Button(mov,text="add",command=callchk1)
    add.pack(pady= 30)
    back = Button(mov,text="back")
    back.pack()
    mov.mainloop()
    messagebox.showinfo("Success", "Successfully Inserted Movie!!")

def addTh():
    th = Tk()
    def goBack():
        th.destroy()
        Admin()
    Button(text="Back", command=goBack).pack()
    th.title("Admin")
    frame = LabelFrame(th, padx=100,pady=100 )
    frame.pack()
    e1 = Entry(frame,width=35,borderwidth=5)
    e1.grid(row = 2,column=3,columnspan=3,padx=10,pady=15)
    e1.insert(0,"Name")
    e2 = Entry(frame, width=35, borderwidth=5)
    e2.grid(row=4, column=3, columnspan=3, padx=10, pady=15)
    e2.insert(0, "pincode")
    e3 = Entry(frame,width=35,borderwidth=5)
    e3.grid(row = 4,column=3,columnspan=3,padx=10,pady=15)
    e3.insert(0,"city")
    e4 = Entry(frame,width=35,borderwidth=5)
    e4.grid(row = 5,column=3,columnspan=3,padx=10,pady=15)
    e4.insert(0,"pincode")
    def callchk1():
        name = e1.get()
        road = e2.get()
        city = e3.get()
        pincode = e4.get()
        mycursor.execute('''insert into theatre(name,road,city,pincode) values(%s,%s,%s,%s)''',(name,road,city,pincode))
        mydb.commit()
        th.destroy()
    add = Button(th,text="add",command=callchk1)
    add.pack(pady= 30)
    back = Button(th,text="back")
    back.pack()
    th.mainloop()
    messagebox.showinfo("Success", "Successfully Inserted Theatre!!")
# mycursor = mydb.cursor()
# mycursor.execute('''select* from theatre''')
# info = mycursor.fetchall()
# for i in info:
#     print(i)

def hallchooseTh():
    hallPg = Tk()
    def goBack():
        hallPg.destroy()
        Admin()
    Button(text="Back", command=goBack).pack()
    Label(text="Choose theatre",font="70").pack()
    mycursor.execute('''select ID,name from theatre''')
    th_info = mycursor.fetchall()
    f = Frame()
    f.pack(padx=200,pady=50)
    R = 1
    r = IntVar()
    for th in th_info:
        Radiobutton(f, font="50", variable=r, value=th[0]).grid(row=R, column=0)
        Label(f, text=th[1], font="50").grid(row=R, column=1)
        R = R + 1
    def clicked(ID):
        if(ID==0):
            print("Error", "Please select a theatre")
        else:
            hallPg.destroy()
            hallchooseCap(ID)
    Button(text="Proceed",command=lambda :clicked(r.get())).pack()
    hallPg.mainloop()


def hallchooseCap(ID):
    hallPg = Tk()
    def goBack():
        hallPg.destroy()
        hallchooseTh()
    Button(text="Back", command=goBack).pack()
    Label(text="Enter hall capacity",font="100",padx=100,pady=100).pack()
    e = Entry()
    e.pack()
    def clicked():
        val = e.get()
        mycursor.execute('''insert into hall(theatre_ID,capacity) values(%s,%s)''',(ID,val))
        mydb.commit()
        hallPg.destroy()
    Button(text="Proceed",font="50",command=clicked,padx=100,pady=20).pack()
    hallPg.mainloop()
    messagebox.showinfo("Success", "Successfully Inserted Hall!!")

def chooseShowMovie():
    movPg = Tk()
    def goBack():
        movPg.destroy()
        Admin()
    Button(text="Back", command=goBack).pack()
    Label(text="Choose Movie",font="50").pack()
    frame = Frame(movPg)
    frame.pack()
    mycursor.execute('select ID,name from movie')
    lst = mycursor.fetchall()
    r = IntVar()
    for k in lst:
        rb = Radiobutton(frame, text=k[1], font="50", variable=r, value=k[0],padx=100).pack()
    def clicked(mov_ID):
        if (mov_ID == 0):
            messagebox.showinfo("Error", "Please select a movie")
        else:
            movPg.destroy()
            chooseShowTheatre(mov_ID)
    Button(text="Proceed",font="50",command=lambda :clicked(r.get())).pack()
    movPg.mainloop()

def chooseShowTheatre(mov_ID):
    thtPg = Tk()
    def goBack():
        thtPg.destroy()
        chooseShowMovie()
    Button(text="Back", command=goBack).pack()
    Label(text="Choose Theatre", font="50").pack()
    frame = Frame(thtPg)
    frame.pack()
    mycursor.execute('select ID,name from theatre')
    lst = mycursor.fetchall()
    r = IntVar()
    for k in lst:
        rb = Radiobutton(frame, text=k[1], font="50", variable=r, value=k[0],padx=100).pack()
    def clicked(t_ID):
        if(t_ID==0):
            messagebox.showinfo("Error","Please select a theatre")
        else:
            thtPg.destroy()
            chooseShowHall(mov_ID,t_ID)
    Button(text="Proceed",command=lambda:clicked(r.get())).pack()
    thtPg.mainloop()

def chooseShowHall(mov_ID,t_ID):
    hallPg = Tk()
    def goBack():
        hallPg.destroy()
        chooseShowTheatre(mov_ID)

    Button(text="Back", command=goBack).pack()
    Label(text="Choose Theatre", font="50").pack()
    frame = Frame(hallPg)
    frame.pack()
    mycursor.execute('select ID,capacity from hall where theatre_ID=%s',(t_ID,))
    lst = mycursor.fetchall()
    r = IntVar()
    for k in lst:
        rb = Radiobutton(frame, text=str(k[0])+"  capacity:"+str(k[1]), font="50", variable=r, value=k[0],padx=100).pack()

    def clicked(h_ID):
        if (h_ID == 0):
            messagebox.showinfo("Error", "Please select a hall")
        else:
            hallPg.destroy()
            enterStartTime(mov_ID,t_ID,h_ID)

    Button(text="Proceed", command=lambda: clicked(r.get())).pack()
    hallPg.mainloop()

def enterStartTime(mov_ID,t_ID,h_ID):
    timePg = Tk()
    def goBack():
        timePg.destroy()
        chooseShowHall(mov_ID,h_ID)
    Button(text="back",font="50",command=goBack).pack()
    Label(text="Enter Start Time(HH:MM:SS)",font="50").pack()
    e1 = Entry()
    e1.pack()
    Label(text="Enter Date(YYYY-MM-DD)", font="50").pack()
    e2 = Entry()
    e2.pack()
    Label(text="Enter Price", font="50").pack()
    e3 = Entry()
    e3.pack()
    def clicked():
        val1 = e1.get()
        val2 = e2.get()
        val3 = e3.get()
        mycursor.execute('''select length from movie where ID=%s''',(mov_ID,))
        length = mycursor.fetchall()
        length = length[0][0]
        mycursor.execute('''select cast(%s as time)+cast(%s as time)''', (val1, length))
        chk = mycursor.fetchall()
        chk = chk[0][0]
        if(chk>=240000):
            chk=0
        else:
            chk=1
        mycursor.execute('''select cast(cast(%s as time)+cast(%s as time) as time)''',(val1,length))
        en_time = mycursor.fetchall()
        en_time = en_time[0][0]
        if(chk==0):
            messagebox.showinfo("Error","Invalid Entry/Show goes beyond 12 AM")
        else:
            mycursor.execute('''select cast(%s as time)''',(val1,))
            val1 = mycursor.fetchall()
            val1 = val1[0][0]
            mycursor.execute('''select cast(%s as date)''', (val2,))
            val2 = mycursor.fetchall()
            val2 = val2[0][0]
            mycursor.execute('''select cast(%s as time)''', (en_time,))
            en_time = mycursor.fetchall()
            en_time = en_time[0][0]
            mycursor.execute('''select* from shows''')
            info = mycursor.fetchall()
            for i in info:
                if(mov_ID==i[1] and t_ID==i[2] and h_ID==i[3] and str(val2)==str(i[6])):
                    if((val1<=i[4] and i[4]<=en_time)or(val1<=i[5] and i[5]<=en_time)or
                        (i[4]<=val1 and val1<=i[5])or(i[4]<=en_time and en_time<=i[5])):
                        messagebox.showinfo("Error","Clash")
                        chk=0
                        break
            if(chk==1):
                mycursor.execute('''insert into shows(movie_ID,hall_ID,theatre_ID,start_time,end_time,show_date,price) values
                                    (%s,%s,%s,%s,%s,%s,%s)''',(mov_ID,h_ID,t_ID,val1,en_time,val2,val3))
                mydb.commit()
                timePg.destroy()
                messagebox.showinfo("Success","Successfully Inserted Show!!")


    Button(text="Proceed",font="50",command=clicked).pack()
    timePg.mainloop()

def Admin():
    root = Tk()
    def movie():
        root.destroy()
        addMov()
    def theatre():
        root.destroy()
        addTh()
    def hall():
        root.destroy()
        hallchooseTh()
    def show():
        root.destroy()
        chooseShowMovie()
    Button(text="Add Movie",font="50",command=movie,padx=100).pack()
    Button(text="Add Theatre", font="50", command=theatre,padx=100).pack()
    Button(text="Add Hall", font="50", command=hall,padx=100).pack()
    Button(text="Add Show",font="50",command=show,padx=100).pack()
    root.mainloop()
Admin()





