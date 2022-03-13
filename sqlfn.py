pwd = "manager"
db = 'mvm'


def columns():
    import mysql.connector as ms
    mycom=ms.connect(host='localhost',user='root',password=pwd
                 ,database=db)
    cur=mycom.cursor()
    cur.execute("select Column_name from INFORMATION_SCHEMA.COLUMNS where TABLE_NAME='attn';")
    return cur.fetchall()
    mycom.close()


def history():
    import mysql.connector as ms
    mycom=ms.connect(host='localhost',user='root',password=pwd
                 ,database=db)
    cur=mycom.cursor()
    cur.execute("select * from attn;")
    return cur.fetchall()
    mycom.close()


def extractdate():
    import mysql.connector as ms
    mycom=ms.connect(host='localhost',user='root',password=pwd
                 ,database=db)
    cur=mycom.cursor()
    cur.execute("select curdate();")
    return str(cur.fetchone()).lstrip('(datetime.date(').rstrip('),)').replace(', ','-')
    mycom.close()

def no_students():
    import mysql.connector as ms
    mycom=ms.connect(host='localhost',user='root',password=pwd
                 ,database=db)
    cur=mycom.cursor()
    cur.execute("desc attn;")
    st=cur.fetchall()
    mycom.close()
    return len(st)-1

def add_students():
    try:
        import mysql.connector as ms
        mycom=ms.connect(host='localhost',user='root',password=pwd
                 ,database=db)
        cur=mycom.cursor()
        while True:
            if input('Do you want to exit? (y-yes,n-no): ')=='y':
                break
            cur.execute("alter table attn\
                add({} varchar(30))".format(input('enter student name:')))
            mycom.commit()
        mycom.close()
    except:
        print('sorry, an error occured')

def add_date(date=extractdate()):
    try:
        import mysql.connector as ms
        mycom=ms.connect(host='localhost',user='root',password=pwd
                 ,database=db)
        cur=mycom.cursor()
        l=[date]
        for i in range(no_students()):
            l.append('absent')
        cur.execute("insert into attn values{};".format(tuple(l)))
        mycom.commit()
        mycom.close()
    except:
        print('date already exists')
        mycom.close()

def attendance(date=extractdate()):
    try:
        import mysql.connector as ms
        mycom=ms.connect(host='localhost',user='root',password=pwd
                     ,database=db)
        cur=mycom.cursor()
        cur.execute("select * from attn where dates='{}';".format(date))
        at=cur.fetchone().count('present')
        mycom.close()
        return at
    except:
        print('date not found')

def mark_present(name,date=extractdate()):
    import mysql.connector as ms
    mycom=ms.connect(host='localhost',user='root',password=pwd
                 ,database=db)
    cur=mycom.cursor()
    cur.execute("update attn \
    set {}='present' \
    where dates='{}';".format(name,date))
    mycom.commit()
    mycom.close()
