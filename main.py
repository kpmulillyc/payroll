from flask import Flask, render_template,request,jsonify,url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import  and_
from sqlalchemy.sql import func
import uniout
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:kingsford@localhost/payroll?charset=utf8'
db=SQLAlchemy(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True


def checkMonth(x):
    if x in ("1", "3", "5", "7", "8", "10", "12"):
        return True
    else:
        return False

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
    id = db.Column(db.Integer, primary_key=True)
    employeeid = db.Column(db.Integer, db.ForeignKey('employee.id'))
    date = db.Column(db.Date)
    amount = db.Column(db.DECIMAL(10,2))

    def __init__(self, employeeid,date,amount):
        self.employeeid = employeeid
        self.date = date
        self.amount = amount


class DailySalary(db.Model):
    __tablename__='dailySalary'
    id = db.Column(db.Integer, primary_key=True)
    employeeid = db.Column(db.Integer, db.ForeignKey('employee.id'))
    date = db.Column(db.Date)
    amount = db.Column(db.DECIMAL(10,2))

    def __init__(self, employeeid,date,amount):
        self.employeeid = employeeid
        self.date = date
        self.amount = amount



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

@app.route('/calculate/<id>')
def calculate(id):
    worker = db.session.query(Employee).filter(Employee.hkid==id).first()
    a = db.session.query(Employee,DailySalary).filter(and_(func.MONTH(DailySalary.date)==11),Employee.id==DailySalary.employeeid).all()
    return render_template("calculate.html", id = id, wages = a, worker= worker)

@app.route('/newsalary/<id>')
def newsalary(id):
    worker = db.session.query(Employee).filter(Employee.hkid==id).first()
    return render_template("newsalary.html",id=id, worker=worker)


@app.route('/pay', methods=['POST','GET'])
def pay():

    day=[]
    employeeid = request.form['employeeid']
    month = str(11)
    year = str(2016)
    col = "-"
    sum = request.form['sum']
    if checkMonth(month):
        for i in range(31):
            day.append(request.form['day'+str(i+1)])
            date = str(i+1)
            date_string = year+col+month+col+date
            datetime.strptime(date_string, "%Y-%m-%d")
            a = Salary(employeeid,datetime.now(),sum)
            b = DailySalary(employeeid, date_string, day[i] )
            db.session.add(b)
        db.session.add(a)
        db.session.commit()
    else:
        for i in range(30):
            day.append(request.form['day'+str(i+1)])
            date = str(i+1)
            date_string = year+col+month+col+date
            datetime.strptime(date_string, "%Y-%m-%d")
            a = Salary(employeeid, datetime.now(),sum)
            b = DailySalary(employeeid, date_string, day[i] )
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