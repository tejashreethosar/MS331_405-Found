from flask import Flask, render_template, Response,session,url_for
from flask import Flask, flash, redirect, render_template, request, abort
from flask_mail import Mail, Message
import pandas as pd
import json
from inference import pose
from HandgestureOpenCv import handGes
from face_recog1 import predict
from tester import weapDetect
from camera import VideoCamera
from pieexp import expRes
from piehand import handRes
from piepose import poseRes
from pieface import faceRes

app = Flask(__name__,template_folder='templates')
app.secret_key = "abc"
mail= Mail(app)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'shreyaswaitforitdorle@gmail.com'
app.config['MAIL_PASSWORD'] = 'doyoufeelincharge'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


@app.route('/')
def home():
        return render_template('/login.html')


@app.route('/famatch',methods=['POST'])
def faceindex():
    if request.form['action'] == 'Video':
        session['path'] = request.form['path3']
        s=session['path']
    elif request.form['action'] == 'Camera':
        session['path'] = 0
        s=session['path']
    
    # s=session['path']
    # isWeap=weapDetect(s)
    id1=predict(s)
    if(id1==1):
        return render_template('/weapon.html')
    else:
        return render_template('/fail.html')

    # if (id1=="unknown"):
    #     return render_template('/fail.html')
    # ehand

# @app.route('/main_weap', methods=['GET', 'POST'])
# def weap_main():
#     # # if request.method == 'POST':
#     # if request.method == 'POST':
#     #     user = request.form['nm']
#     return redirect(url_for('whome'))
    # else:
    #     # return render_template('/upload.html')

@app.route('/weapon',methods=['POST'])
def whome():
    w=session['path']
    isWeap=weapDetect(w)
    if (isWeap==1):
        msg = Message('Weapon Detected', sender = 'shreyaswaitforitdorle@gmail.com', recipients = ['shreyasdorle.it@gmail.com'])
        msg.body = "Weapon has been detected at given location!"
        mail.send(msg)
        return render_template('/fail2.html')
    else:
        return render_template('/pose.html')

@app.route('/pose',methods=['POST'])
def home1():
    # varpath1 = request.form['path1']
    varpath1=session['path']
    isPose=pose(varpath1)
    return render_template('/hand.html')

@app.route('/hand',methods=['POST'])
def home2():
    # varpath2 = request.form['path2']
    varpath2=session['path']
    isGes=handGes(varpath2)
    return render_template('/expr.html')


@app.route('/expr',methods=['POST'])
def index():
    return render_template('/index.html') 

# @app.route('/goexpr',methods=['POST'])
# def index9():
#     return render_template('/expr.html')

# @app.route('/gohand',methods=['POST'])
# def index8():
#     return render_template('/hand.html')     

# @app.route('/gopose',methods=['POST'])
# def index7():
#     return render_template('/pose.html')

# @app.route('/goweap',methods=['POST'])
# def index6():
#     return render_template('/weapon.html')            



# @app.route('/result',methods=['POST'])
# def inex():
#     return render_template('/indexop.html')

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/result',methods=['POST'])
def inex():
    return render_template('/results.html')

# @app.route('/main_pose', methods=['GET', 'POST'])
# def hand_form():
#     # if request.method == 'POST':
#     return redirect(url_for('home1'))

@app.route('/resexpr')
def index11():
    pop1=expRes()
    return render_template('/results.html')

@app.route('/reshand')
def index22():
    pop2=handRes()
    return render_template('/results.html')

@app.route('/respose')
def index33():
    pop3=poseRes()
    return render_template('/results.html')

@app.route('/resface')
def index55():
    pop4=faceRes()
    return render_template('/results.html')

@app.route('/face_form', methods=['GET', 'POST'])
def face_form():
    # if request.method == 'POST':
    return redirect(url_for('index55'))

@app.route('/pose_form', methods=['GET', 'POST'])
def pose_form():
    # if request.method == 'POST':
    return redirect(url_for('index33'))

@app.route('/expr_form', methods=['GET', 'POST'])
def expr_form():
    # if request.method == 'POST':
    return redirect(url_for('index11'))

@app.route('/hand_form', methods=['GET', 'POST'])
def hand_form():
    # if request.method == 'POST':
    return redirect(url_for('index22'))

@app.route('/exp/<name>')
def express1(name):
    df = pd.read_csv (r'isExp.csv')
    df.to_json (r'isExp.json')
    with open('isExp.json', 'r') as jsonfile:
        file_data = json.loads(jsonfile.read())
    return json.dumps(file_data[name])

@app.route('/face/<name>')
def express2(name):
    df = pd.read_csv (r'isFace.csv')
    df.to_json (r'isFace.json')
    with open('isFace.json', 'r') as jsonfile:
        file_data = json.loads(jsonfile.read())
    return json.dumps(file_data[name])

@app.route('/hand/<name>')
def express3(name):
    df = pd.read_csv (r'isHand.csv')
    df.to_json (r'isHand.json')
    with open('isHand.json', 'r') as jsonfile:
        file_data = json.loads(jsonfile.read())
    return json.dumps(file_data[name])

@app.route('/pose/<name>')
def express4(name):
    df = pd.read_csv (r'isPose.csv')
    df.to_json (r'isPose.json')
    with open('isPose.json', 'r') as jsonfile:
        file_data = json.loads(jsonfile.read())
    return json.dumps(file_data[name])

@app.route('/weap/<name>')
def express5(name):
    df = pd.read_csv (r'isWeap.csv')
    df.to_json (r'isWeap.json')
    with open('isWeap.json', 'r') as jsonfile:
        file_data = json.loads(jsonfile.read())
    return json.dumps(file_data[name])


if __name__ == '__main__':
    app.run(debug=True,host='127.0.0.1', port=5000)
