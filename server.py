from flask import Flask, render_template, request, redirect, session
import random 

app = Flask(__name__)
app.secret_key = 'keep it secret, keep it safe'

@app.route('/')
def start():
    if 'winners' not in session:
      session['winners'] = []
    session['number'] = random.randint(1, 5)
    session['result'] = ""
    session['message'] = ""
    session['intentos'] = 0
    return render_template('/index.html') 

@app.route('/guess',methods=["POST"])
def guess():
    numForm = 0
    if request.form["guess"] == "":
      numForm = 0
    else:
      numForm = int(request.form["guess"])
    
    if session['number'] > numForm:
      session['result'] = "wrong"
      session['message'] = "Too low!"
      session['intentos'] += 1
    elif session['number'] < numForm:
      session['result'] = "wrong"
      session['message'] = "Too high!"
      session['intentos'] += 1
    elif session['number'] == numForm:
      session['intentos'] += 1
      session['result'] = "correct"
      session['message'] = f"You guess the correct number! : {session['number']} after {session['intentos']} attempts"
    return render_template('/index.html') 
    
    
@app.route('/saveScore',methods=["POST"])
def save():
    name = request.form["name"]
    b = session['winners'][:]
    b.append({"name": name, "intentos": session['intentos']})
    session['winners'] = b
    print(session['winners'])
    return redirect('/showScores')

@app.route('/showScores')
def scores():
    print(session['winners'])
    b = session['winners'][:]
    b.sort(key=lambda x: x["intentos"], reverse=False)
    session['winners'] = b
    return render_template('/scores.html')

if __name__=="__main__":
    app.run(debug=True)
