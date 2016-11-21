from flask import Flask, render_template,request,jsonify,url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import  and_
from sqlalchemy.sql import func
from ics import icalendar
from datetime import datetime
from urllib import urlopen

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:kingsford@localhost/payroll?charset=utf8'
db=SQLAlchemy(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True



class Employee(db.Model):
    __tablename__ = 'employee'
    id = db.Column(db.Integer, primary_key=True)
    cname = db.Column(db.String(50,collation = 'utf8_bin'))
    ename = db.Column(db.String(50))
    hkid = db.Column(db.String(20))
    address = db.Column(db.String(100))
    phoneM = db.Column(db.Integer)
    phoneH = db.Column(db.Integer)
    salary = db.Column(db.DECIMAL(10,2))
    title = db.Column(db.String(20))
    married = db.Column(db.String(10))
    gender = db.Column(db.String(10))
    eType = db.Column(db.String(10))
    eDate = db.Column(db.Date)
    probation = db.Column(db.String(10))
    probationDays = db.Column(db.Integer)
    probationWeeks = db.Column(db.Integer)
    probationMonths = db.Column(db.Integer)
    remarks = db.Column(db.String(500))
    salaries = db.relationship('Salary', backref='employee',
                                lazy='dynamic')
    dailySalaries = db.relationship('DailySalary', backref='employee',
                               lazy='dynamic')
    def __init__(self, cname, ename, hkid, address, phoneM, phoneH, salary, title, married, gender, eType, eDate, probation, probationDays, probationWeeks, probationMonths, remarks):
        self.cname = cname
        self.ename = ename
        self.hkid = hkid
        self.address = address
        self.phoneM = phoneM
        self.phoneH = phoneH
        self.salary = salary
        self.title = title
        self.married = married
        self.gender = gender
        self.eType = eType
        self.eDate = eDate
        self.probation = probation
        self.probationDays = probationDays
        self.probationWeeks = probationWeeks
        self.probationMonths = probationMonths
        self.remarks = remarks

class Salary(db.Model):
    __tablename__='salary'
    id = db.Column(db.String(255), primary_key=True)
    employeeid = db.Column(db.Integer, db.ForeignKey('employee.id'))
    date = db.Column(db.Date)
    amount = db.Column(db.DECIMAL(10,2))

    def __init__(self,id, employeeid,date,amount):
        self.id = id
        self.employeeid = employeeid
        self.date = date
        self.amount = amount


class DailySalary(db.Model):
    __tablename__='dailySalary'
    id = db.Column(db.String(255), primary_key=True)
    employeeid = db.Column(db.Integer, db.ForeignKey('employee.id'))
    overTime = db.Column(db.DECIMAL(10, 2))
    otHours = db.Column(db.DECIMAL(10,2))
    basicSalary = db.Column(db.DECIMAL(10,2))
    date = db.Column(db.Date)
    dailySalary = db.Column(db.DECIMAL(10,2))
    def __init__(self,id, employeeid,overTime,otHours,basicSalary,date,dailySalary):
        self.id = id
        self.employeeid = employeeid
        self.overTime = overTime
        self.otHours = otHours
        self.basicSalary = basicSalary
        self.date = date
        self.dailySalary = dailySalary


def Holiday(x):
    url = 'http://www.1823.gov.hk/common/ical/tc.ics'
    c = icalendar.Calendar(urlopen(url).read().decode('utf-8'))
    e= icalendar.Event()
    result = False
    e.begin = x
    for i in c.events:
        if e.begin == i.begin:
            result = True
            break
    return result

def showHoliday(x):
    url = 'http://www.1823.gov.hk/common/ical/tc.ics'
    c = icalendar.Calendar(urlopen(url).read().decode('utf-8'))
    e = icalendar.Event()
    e.begin = x
    display = ""
    for i in c.events:
        if e.begin == i.begin:
            display = i.name
    return display

def weekDay(x):
    if x == 0:
        return "Mon"
    elif x == 1:
        return "Tue"
    elif x == 2:
        return "Wed"
    elif x == 3:
        return "Thur"
    elif x == 4:
        return "Fri"
    elif x == 5:
        return "Sat"
    elif x == 6:
        return "<font color='red'>Sun</font>"



@app.route('/')
def index():
    return render_template("index.html")

@app.route('/add')
def add():
    return render_template("add.html")

@app.route('/blank')
def blank():
    return render_template("blank.html")

@app.route('/buttons')
def buttons():
    return render_template("buttons.html")

@app.route('/flot')
def flot():
    return render_template("flot.html")

@app.route('/forms')
def forms():
    return render_template("forms.html")

@app.route('/grid')
def grid():
    return render_template("grid.html")

@app.route('/icons')
def icons():
    return render_template("icons.html")

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/morris')
def morris():
    return render_template("morris.html")

@app.route('/notifications')
def notifications():
    return render_template("notifications.html")

@app.route('/panels-wells')
def panelswells():
    return render_template("panels-wells.html")

@app.route('/tables')
def tables():
    return render_template("tables.html")

@app.route('/employees')
def employees():
    return render_template("employees.html", workers=Employee.query.all())

@app.route('/wages')
def wages():
    return render_template("wages.html", workers=Employee.query.all())

@app.route('/employees/<id>')
def edit(id):
    worker = Employee.query.filter_by(hkid=id).first()
    return render_template("edit.html", worker=worker)

@app.route('/typography')
def typography():
    return render_template("typography.html")

@app.route('/report/<id>')
def report(id):
    worker = Employee.query.filter_by(hkid=id).first()
    a = worker.salaries.all()
    return render_template("report.html", id = id, wages = a, worker= worker)

@app.route('/calculate/<id>?<date>')
def calculate(id,date):
    date = datetime.strptime(date,"%Y-%m-%d")
    worker = db.session.query(Employee).filter(Employee.hkid==id).first()
    a = db.session.query(Employee,DailySalary).filter(and_(func.MONTH(DailySalary.date)==func.MONTH(date),func.YEAR(DailySalary.date)==func.YEAR(date),worker.id==DailySalary.employeeid)).all()
    b = db.session.query(Salary).filter(and_(func.MONTH(Salary.date)==func.MONTH(date),func.YEAR(date)==func.YEAR(Salary.date),worker.id==Salary.employeeid)).all()
    strdate = datetime.strftime(date,"%m-%Y")
    wd = []
    for i in a:
        hddd = datetime.strftime(i.DailySalary.date, "%Y%m%d") + " 00:00:00"
        if Holiday(hddd):
            wd.append('<font color="red">'+showHoliday(hddd)+'</font>')
        else:
            wd.append(weekDay(i.DailySalary.date.weekday()))
    return render_template("calculate.html", id = id, wages = a, worker= worker,date=strdate, wd=wd, mt=b)

@app.route('/newsalary/<id>',methods = ['POST','GET'])
def newsalary(id):
    worker = db.session.query(Employee).filter(Employee.hkid==id).first()
    if request.is_xhr:
        days = int(request.form['days'])
        month = str(request.form['month'])
        year = str(request.form['year'])
        new = ''
        check = db.session.query(Employee,Salary).filter(and_(func.YEAR(Salary.date)==int(year),func.MONTH(Salary.date)==int(month),Salary.employeeid==worker.id)).first()
        if check is not None:
            exist= "Record already exist"
            return jsonify(exist=exist,new=new)
        else:
            for x in range(days):
                ddd = datetime.strptime((year+":"+month+":"+str(x+1)),"%Y:%m:%d")
                hddd = datetime.strftime(ddd,"%Y%m%d")+" 00:00:00"
                wd = ddd.weekday()
                if Holiday(hddd):
                    html = '<tr><td>' + str(x + 1) + '&nbsp;&nbsp;&nbsp; <font color="red">'+showHoliday(hddd)+'</font>'\
                        '<input type="hidden" id="ratio' + str(x + 1) + '" value="2"></td>' \
                        '<td><input class="form-control" value ="0.00" id="bs' + str(x + 1) + '"></td>'\
                        '<td><input class="form-control" value ="0.00" id="ot' + str(x + 1) + '" readonly></td>' \
                        '<td><input class="form-control" value ="0" name="hot" id="hot' + str(x + 1) + '"></td>' \
                        '<td><input class="form-control" name="txt" value ="0.00" id="ds' + str(x + 1) + '" readonly></td></tr>'
                elif wd is not 6:
                    html = '<tr><td>'+str(x+1)+'&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'+weekDay(wd)+'<input type="hidden" id="ratio'+str(x+1)+'" value="1.5"></td>'\
                           '<td><input class="form-control" value ="0.00" id="bs'+str(x+1)+'"></td>'\
                           '<td><input class="form-control" value ="0.00" id="ot'+str(x+1)+'" readonly></td>' \
                           '<td><input class="form-control" value ="0" name="hot" id="hot'+str(x+1)+'"></td>' \
                           '<td><input class="form-control" name="txt" value ="0.00" id="ds'+str(x+1)+'" readonly></td></tr>'
                else:
                    html = '<tr><td>'+str(x+1)+'&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'+weekDay(wd)+'<input type="hidden" id="ratio'+str(x+1)+'" value="2"></td>'\
                        '<td><input class="form-control" value ="0.00" id="bs' + str(x+1) + '"></td>' \
                        '<td><input class="form-control" value ="0.00" id="ot' + str(x + 1) + '" readonly></td>' \
                        '<td><input class="form-control" value ="0" name="hot" id="hot' + str(x + 1) + '"></td>' \
                        '<td><input class="form-control" name="txt" value ="0.00" id="ds' + str(x + 1) + '" readonly></td></tr>'
                new += html
                exist="New record"
            return jsonify(exist=exist,new=new)
    else:
        return render_template("newsalary.html", worker=worker)


@app.route('/pay', methods=['POST','GET'])
def pay():
    bs=[]
    ot=[]
    ds=[]
    hot=[]
    employeeid = request.form['employeeid']
    month = request.form['month']
    year = request.form['year']
    sum = request.form['sum']
    col = ":"
    days=int(request.form['days'])
    sumdatestr = year+col+month+col+"1"
    sumdate = datetime.strptime(sumdatestr, "%Y:%m:%d")
    id = str(employeeid+'-'+sumdatestr)
    a = Salary(id, employeeid, sumdate, sum)
    for i in range(days):
        bs.append(request.form['bs' + str(i + 1)])
        ot.append(request.form['ot' + str(i + 1)])
        ds.append(request.form['ds'+str(i+1)])
        hot.append(request.form['hot'+str(i+1)])
        date_string = year+col+month+col+str(i+1)
        daystr = datetime.strptime(date_string, "%Y:%m:%d")
        id =  str(daystr) + "-" + str(employeeid)
        b = DailySalary(id,employeeid, ot[i],hot[i],bs[i], daystr, ds[i])
        db.session.add(b)
    db.session.add(a)
    db.session.commit()
    bbb='done'
    return jsonify(bbb=bbb)



@app.route('/addEmployee', methods=['POST','GET'])
def addEmployee():
    gender = request.form['gender']
    married = request.form['marriage']
    eType = request.form['type']
    eDate = request.form['eDate']
    hkid = request.form['idnum']
    cname = request.form['chinese']
    ename = request.form['english']
    address = request.form['address']
    phoneH = request.form['home']
    phoneM = request.form['mobile']
    salary = request.form['salary']
    title = request.form['title']
    probation = request.form['probation']
    if probation is "No":
        probationDays = 0
        probationWeeks = 0
        probationMonths = 0
    else:
        probationDays = request.form['pd']
        probationWeeks = request.form['pw']
        probationMonths = request.form['pm']
    remarks = request.form['remarks']
    if Employee.query.filter_by(hkid=hkid).first() is None:
        newEmployee = Employee(cname, ename, hkid, address, phoneM, phoneH, salary, title, married, gender, eType, eDate, probation, probationDays, probationWeeks, probationMonths, remarks)
        db.session.add(newEmployee)
        db.session.commit()
        bbb = "Successfully added!"
    else:
        bbb = "Employee already exists!"
    print (cname, ename, hkid, address, phoneM, phoneH, salary, title, married, gender, eType, eDate, probation, remarks)
    return jsonify(bbb=bbb)



@app.route('/updateEmployee', methods=['POST','GET'])
def updateEmployee():
    workerid = request.form['workerid']
    print (workerid)
    upTarget = Employee.query.filter_by(hkid=workerid).first()
    upTarget.gender = request.form['gender']
    upTarget.married = request.form['marriage']
    upTarget.eType = request.form['type']
    upTarget.eDate = request.form['eDate']
    upTarget.hkid = request.form['idnum']
    upTarget.cname = request.form['chinese']
    upTarget.ename = request.form['english']
    upTarget.address = request.form['address']
    upTarget.phoneH = request.form['home']
    upTarget.phoneM = request.form['mobile']
    upTarget.salary = request.form['salary']
    upTarget.title = request.form['title']
    upTarget.probation = request.form['probation']
    if upTarget.probation is "No":
        upTarget.probationDays = 0
        upTarget.probationWeeks = 0
        upTarget.probationMonths = 0
    else:
        upTarget.probationDays = request.form['pd']
        upTarget.probationWeeks = request.form['pw']
        upTarget.probationMonths = request.form['pm']
    upTarget.remarks = request.form['remarks']
    db.session.commit()
    return jsonify(bbb="Updated!")



if __name__ == '__main__':
    app.run(debug=True,threaded=True)