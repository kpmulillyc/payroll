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
    hkid = db.Column(db.String(20), unique = True)
    address = db.Column(db.String(100))
    phoneM = db.Column(db.Integer)
    phoneH = db.Column(db.Integer)
    salary = db.Column(db.Float)
    title = db.Column(db.String(20))
    '''married 1 = single, 2 = married'''
    married = db.Column(db.String(10))
    '''gender 1 = male , 2 = female'''
    gender = db.Column(db.String(10))
    '''eType 1 = hourly, 2 = daily, 3 = monthly'''
    eType = db.Column(db.String(10))
    eDate = db.Column(db.DateTime)
    '''probation 1 = no, 2 =yes'''
    probation = db.Column(db.String(10))
    '''probation time unit in days'''
    probationTime = db.Column(db.Integer)
    remarks = db.Column(db.String(500))
    def __init__(self, cname, ename, hkid, address, phoneM, phoneH, salary, title, married, gender, eType, eDate, probation, probationTime, remarks):
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
        self.probationTime = probationTime
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
    pd= int(request.form['pd'])
    pm=int(request.form['pm'])
    remarks = request.form['remarks']
    newEmployee = employee(cname, ename, hkid, address, phoneM, phoneH, salary, title, married, gender, eType, eDate, probation, pm+pd, remarks)
    db.session.add(newEmployee)
    db.session.commit()
    print (cname, ename, hkid, address, phoneM, phoneH, salary, title, married, gender, eType, eDate, probation, pm+pd, remarks)
    return jsonify(bbb=eDate)




if __name__ == '__main__':
    app.run(debug=True)