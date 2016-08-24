from flask import Flask, render_template,request,jsonify,url_for
from flask_sqlalchemy import SQLAlchemy
import uniout
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:kingsford@localhost/payroll?charset=utf8'
db=SQLAlchemy(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

class employee(db.Model):
    __tablename__ = 'employee'
    id = db.Column(db.Integer, primary_key=True)
    cname = db.Column(db.String(50,collation = 'utf8_bin'))
    ename = db.Column(db.String(50))
    hkid = db.Column(db.String(20))
    address = db.Column(db.String(100))
    phoneM = db.Column(db.Integer)
    phoneH = db.Column(db.Integer)
    salary = db.Column(db.Float)
    title = db.Column(db.String(20))
    married = db.Column(db.String(10))
    gender = db.Column(db.String(10))
    eType = db.Column(db.String(10))
    eDate = db.Column(db.DateTime)
    probation = db.Column(db.String(10))
    probationDays = db.Column(db.Integer)
    probationWeeks = db.Column(db.Integer)
    probationMonths = db.Column(db.Integer)
    remarks = db.Column(db.String(500))
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
    return render_template("employees.html", workers=employee.query.all())


@app.route('/employees/<name>')
def edit(name):
    worker = employee.query.filter_by(ename=name).first()
    return render_template("edit.html", name = name, worker=worker)

@app.route('/typography')
def typography():
    return render_template("typography.html")

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
    probationDays= request.form['pd']
    probationWeeks=request.form['pw']
    probationMonths= request.form['pm']
    remarks = request.form['remarks']
    newEmployee = employee(cname, ename, hkid, address, phoneM, phoneH, salary, title, married, gender, eType, eDate, probation, probationDays, probationWeeks, probationMonths, remarks)
    db.session.add(newEmployee)
    db.session.commit()
    print (cname, ename, hkid, address, phoneM, phoneH, salary, title, married, gender, eType, eDate, probation, remarks)
    return jsonify(bbb=eDate)


@app.route('/updateEmployee', methods=['POST','GET'])
def updateEmployee():
    workerid = request.form['workerid']
    upTarget = employee.query.filter_by(id=workerid).first()
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
    upTarget.probationDays = request.form['pd']
    upTarget.probationWeeks = request.form['pw']
    upTarget.probationMonths = request.form['pm']
    upTarget.remarks = request.form['remarks']
    db.session.commit()
    return jsonify(bbb="gaodim")

if __name__ == '__main__':
    app.run(debug=True)