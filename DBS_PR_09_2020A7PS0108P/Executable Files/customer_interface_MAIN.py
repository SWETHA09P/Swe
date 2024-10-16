from tkinter import *
import mysql.connector
from tkinter import messagebox
mydb = mysql.connector.connect(host="bivpmn8lmtfrb2ckizfa-mysql.services.clever-cloud.com",
                                user="ul7kjuw51idmwufn",
                                passwd="Y59vGTRrnEQaepWvTFQt",
                               database="bivpmn8lmtfrb2ckizfa")
mycursor = mydb.cursor()



# button functions



# page functions
def signuppge():
    signuppg = Tk()
    signuppg.title("movie booking")
    def goBack():
        signuppg.destroy()
        welcomePage()
    Button(text="back",command=goBack).pack()
    frame = LabelFrame(signuppg, padx=100, pady=100)
    frame.pack()
    lable = Label(frame, text="Sign-up", fg="white", bg="blue", padx=15, pady=15).grid(row=0, column=4)
    e = Entry(frame, width=35, borderwidth=5)
    e.grid(row=1, column=3, columnspan=3, padx=10, pady=15)
    e.insert(0, "Name")
    e1 = Entry(frame, width=35, borderwidth=5)
    e1.grid(row=2, column=3, columnspan=3, padx=10, pady=15)
    e1.insert(0, "Email")
    e2 = Entry(frame, width=35, borderwidth=5)
    e2.grid(row=3, column=3, columnspan=3, padx=10, pady=15)
    e2.insert(0, "Enter a Password")

    def callupdate():
        # sql query
        name = e.get()
        email = e1.get()
        password = e2.get()
        mycursor.execute('''select case when exists(select email from customer where email=%s) 
                            then 0 else 1 end as val''',(email,))
        sql_query = mycursor.fetchall()
        sql_query = sql_query[0][0]
        print(sql_query)
        if(sql_query==0):
            messagebox.showinfo("Error", "Email already in use,\nplease use another")
        else:
            mycursor.execute("insert into customer(name,email,password) values(%s,%s,%s)", (name, email, password))
            mydb.commit()
            mycursor.execute('''select max(ID) from customer''')
            custId = mycursor.fetchall()
            custId = custId[0][0]
            signuppg.destroy()
            movies(custId)

    signup1 = Button(frame, text="Sign-up", command=callupdate).grid(row=5, column=4, pady=30)


def loginpge():
    loginpg = Tk()
    loginpg.title("movie booking")
    def goBack():
        loginpg.destroy()
        welcomePage()
    Button(text="back",command=goBack).pack()
    frame = LabelFrame(loginpg, padx=100, pady=100)
    frame.pack()
    lable = Label(frame, text="Login", fg="white", bg="blue", padx=15, pady=15).grid(row=0, column=4)
    e1 = Entry(frame, width=35, borderwidth=5)
    e1.grid(row=2, column=3, columnspan=3, padx=10, pady=15)
    e1.insert(0, "Enter your Email")
    e2 = Entry(frame, width=35, borderwidth=5)
    e2.grid(row=3, column=3, columnspan=3, padx=10, pady=15)
    e2.insert(0, "Enter your Password")

    def callchk():
        email = e1.get()
        password = e2.get()
        mycursor.execute('''select case when (%s in (select distinct email from customer) and 
                                    %s in (select distinct password from customer)) then 1 else 0 end as val''',
                                   (email,password))
        sql_qry = mycursor.fetchone()
        if (sql_qry[0] == 0):
            messagebox.showinfo("Error", "Invalid Credentials! \n Please Try Again...")
        else:
            loginpg.destroy()
            mycursor.execute('''select ID from customer where email=%s and password=%s''',(email,password))
            custId = mycursor.fetchall()
            custId = custId[0][0]
            movies(custId)

    login1 = Button(frame, text="Login", command=callchk).grid(row=5, column=4, pady=30)

def callTheatrePage(movie_id,custId):
    thtpg = Tk()
    def goBack():
        thtpg.destroy()
        movies(custId)
    Button(text="back",command=goBack).pack()
    query = '''select s.ID,t.name,start_time,show_date,hall_ID
               from shows s,theatre t
               where s.movie_ID=%s and s.theatre_ID=t.ID
               order by show_date,start_time'''
    mycursor.execute(query,(movie_id,))
    shows = mycursor.fetchall()
    mycursor.execute('select name from movie where ID=%s',(movie_id,))
    movie_name = mycursor.fetchall()
    movie_name = movie_name[0][0]
    r = IntVar()
    chk=0
    l = Label(text=movie_name,font="200",padx=400).pack()
    def clicked(show_ID):
        if(show_ID==0):
            messagebox.showinfo("Error", "Please select a show")
        else:
            thtpg.destroy()
            seats(show_ID,custId)
    f = Frame()
    f.pack()
    R = 1
    for sh in shows:
        #desc = "\t"+sh[1]+"\t"+str(sh[2])+"\t"+str(sh[3])+"\thall:"+str(sh[4])
        rb = Radiobutton(f,font="50",variable=r,value=sh[0]).grid(row=R,column=0)
        Label(f,text=str(sh[1])+"\t",font="50").grid(row=R,column=1)
        Label(f, text=str(sh[2])+"\t\t",font="50").grid(row=R, column=2)
        Label(f, text=str(sh[3])+"\t",font="50").grid(row=R, column=3)
        Label(f, text="hall:"+str(sh[4]),font="50").grid(row=R, column=4)
        R = R+1

    b = Button(text="Proceed",font="50",command=lambda:clicked(r.get())).pack()
    thtpg.mainloop()

def movies(custID):
    movie = Tk()
    movie.title("movie booking")
    def goBack():
        movie.destroy()
        mycursor.execute('''select max(ID) from customer''')
        maxID = mycursor.fetchall()
        maxID = maxID[0][0]
        if(custID==maxID):
            signuppge()
        else:
            loginpge()
    Button(text="back",command=goBack).pack()
    frame = LabelFrame(movie, padx=100, pady=100)
    frame.pack()
    mycursor.execute('select ID,name from movie')
    lst = mycursor.fetchall()
    lable = Label(frame, text="Select Movie",fg = "white",bg = "blue",padx = 15,pady=15).pack()
    def clicked(id):
        if(id==0):
            messagebox.showinfo("Error","Please select a movie")
        else:
            movie.destroy()
            callTheatrePage(id,custID)
    chk=0
    r = IntVar()
    for k in lst:
        rb = Radiobutton(frame,text = k[1], font="50",variable = r, value = k[0]).pack()
    btn = Button(frame,text="select",command= lambda: clicked(r.get())).pack()


def welcomePage():
    root = Tk()
    root.title("movie booking")
    frame = LabelFrame(root, padx=100, pady=100)
    frame.pack()
    lable = Label(frame, text="Please Sign-up or Login", pady=30).grid(row=0, column=4)
    def signupbtn():
        root.destroy()
        signuppge()

    def loginbtn():
        root.destroy()
        loginpge()
    login = Button(frame, text="Login", command=loginbtn).grid(row=5, column=0)
    signup = Button(frame, text="Sign-up", command=signupbtn).grid(row=5, column=8)
    root.mainloop()

def seats(show_ID,custId):
    mycursor.execute('''select hall_ID,theatre_ID from shows where ID=%s''',(show_ID,))
    info = mycursor.fetchall()
    h_ID = info[0][0]
    t_ID = info[0][1]
    mycursor.execute('''select capacity from hall where ID=%s and theatre_ID=%s''',(info[0][0],info[0][1]))
    info = mycursor.fetchall()
    info = info[0][0]
    seatPage = Tk()
    def goBack():
        seatPage.destroy()
        mycursor.execute('''select movie_ID from shows where ID=%s''',(show_ID,))
        movie_ID = mycursor.fetchall()
        movie_ID = movie_ID[0][0]
        callTheatrePage(movie_ID,custId)
    Button(text="back",command=goBack).pack()
    Label(text="Select a seat",font="200",pady=10).pack()
    Label(text="Green-Avalaible",font="100",padx=50).pack()
    f = Frame(seatPage,padx=100,pady=20)
    f.pack()
    status = []
    chkbtn = []
    mycursor.execute('''select seat_ID from books where show_ID=%s''',(show_ID,))
    data = mycursor.fetchall()
    booked = []
    for i in data:
        booked.append(i[0])
    mycursor.execute('''SELECT seat_ID from seatinline where show_ID=%s and book_date=curdate() 
                        and (cast(curtime() as time)-cast(book_time as time))<=1000''',(show_ID,))
    data = mycursor.fetchall()
    for i in data:
        print("Yes")
        booked.append(i[0])
    for i in range(0,info):
        var = IntVar()
        chk = Checkbutton(f,variable=var,onvalue=1,offvalue=0,padx=10,pady=10,selectcolor="green",fg="white",bg="yellow")
        chkbtn.append(chk)
        status.append(var)
    for i in booked:
        chkbtn[i-1] = Checkbutton(f,state="disabled",padx=10,pady=10,selectcolor="red",bg="yellow")
    R = 0
    C = 0
    for i in range(0,info):
        chkbtn[i].grid(row=R,column=C)
        C = C+1
        if(C>=10):
            C = 0
            R = R+1
    def clicked():
        newBooked = []
        chk = 0
        for i in range(0,len(status)):
            if(status[i].get()==1):
                chk=1
                newBooked.append(i+1)
        if(chk==0):
            messagebox.showinfo("Error", "Please select a seat")
        else:
            seatPage.destroy()
            callPaymentPage(show_ID,newBooked,custId)
    Label(pady=20,text="_________________________________________________________________________________________").pack()
    Button(text="Proceed",padx=50,pady=10,font="100",command=clicked).pack()
    seatPage.mainloop()

def callPaymentPage(show_ID,newBooked,custId):
    for i in newBooked:
        mycursor.execute('''insert into seatinline(seat_ID,show_ID,book_time,book_date) values
                            (%s,%s,curtime(),curdate())''',(i,show_ID))
    mydb.commit()
    payPage = Tk()
    def goBack():
        payPage.destroy()
        seats(show_ID,custId)
    Button(text="back",command=goBack).pack()
    mycursor.execute('''select* from shows where ID=%s''',(show_ID,))
    show_info = mycursor.fetchall()
    mycursor.execute('''select name from movie where ID=%s''', (show_info[0][1],))
    movie_name = mycursor.fetchall()
    movie_name = movie_name[0][0]
    mycursor.execute('''select name from theatre where ID=%s''', (show_info[0][3],))
    theatre_name = mycursor.fetchall()
    theatre_name = theatre_name[0][0]
    Label(text="Payment",font="500",padx=200,bg="green",fg="white").pack()
    f = Frame(payPage,bg="grey")
    f.pack()
    fl_amt = int(show_info[0][7])*len(newBooked)
    amt = str(fl_amt)
    def clicked():
        payPage.destroy()
        mycursor.execute('''insert into payment(amt,pay_time,pay_date)
                            values(%s,curtime(),curdate())''',(fl_amt,))
        mydb.commit()
        mycursor.execute('''select max(ID) from payment''')
        pay_ID = mycursor.fetchall()
        pay_ID = pay_ID[0][0]
        for i in newBooked:
            mycursor.execute('''insert into books
                                 values(%s,%s,%s,%s)''',(custId,i,show_ID,pay_ID))
        mydb.commit()
        messagebox.showinfo("Message","Payment is successful!")
        for i in newBooked:
            mycursor.execute('''delete from seatinline where seat_ID=%s and show_ID=%s''',(i,show_ID))
        mydb.commit()
    Label(f,text="Movie:",font="50",padx=200,bg="grey").grid(row=1)
    Label(f,text="Hall:",font="50",padx=200,bg="grey").grid(row=2)
    Label(f,text="Theatre:",font="50",padx=200,bg="grey").grid(row=3)
    Label(f,text="Start Time:", font="50", padx=200,bg="grey").grid(row=4)
    Label(f,text="End Time:", font="50", padx=200,bg="grey").grid(row=5)
    Label(f,text="Date:", font="50", padx=200,bg="grey").grid(row=6)
    Label(f,text="Price:", font="50", padx=200,bg="grey").grid(row=7)
    Label(f,text="Seat numbers:",font="50", padx=200,bg="grey").grid(row=8)
    Label(f,text=movie_name, font="50", padx=200,bg="grey").grid(row=1,column=1)
    Label(f,text=show_info[0][2], font="50", padx=200,bg="grey").grid(row=2,column=1)
    Label(f,text=theatre_name, font="50", padx=200,bg="grey").grid(row=3,column=1)
    Label(f,text=show_info[0][4], font="50", padx=200,bg="grey").grid(row=4,column=1)
    Label(f,text=show_info[0][5], font="50", padx=200,bg="grey").grid(row=5,column=1)
    Label(f,text=show_info[0][6], font="50", padx=200,bg="grey").grid(row=6,column=1)
    Label(f,text=amt, font="50", padx=200,bg="grey").grid(row=7,column=1)
    desc = ""
    for i in newBooked:
        desc += "  "+str(i)
    Label(f, text=desc, font="50", padx=200, bg="grey").grid(row=8, column=1)
    b = Button(payPage,command = clicked,text="Pay",font="50",bg="green",fg="white")
    b.pack()
    payPage.mainloop()


# mycursor.execute('''drop if exists seatinline''')
# mycursor.execute('''create table seatinline(
# 					ID int not null auto_increment,
#                     seat_ID int not null,
#                     hall_ID int not null,
#                     theatre_ID int not null,
#                     book_time time not null,
#                     book_date date not null,
#                     primary key(ID)
#                     )''')
welcomePage()

