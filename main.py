from flask import Flask, render_template,request,jsonify
import uniout

app = Flask(__name__)

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

@app.route('/typography')
def typography():
    return render_template("typography.html")

@app.route('/addEmployee')
def addEmployee():
    gender = request.args.get('gender')
    marriage = request.args.get('marriage')
    type = request.args.get('type')
    idnum = request.args.get('idnum')
    chinese = request.args.get('chinese')
    english = request.args.get('english')
    address = request.args.get('address')
    home = request.args.get('home')
    mobile = request.args.get('mobile')
    salary = request.args.get('salary')
    title = request.args.get('title')
    remarks = request.args.get('remarks')
    print (gender,marriage,type,idnum,chinese,english,address,home,mobile,salary,title,remarks)
    return jsonify(data="hello r")


if __name__ == '__main__':
    app.run(debug=True)