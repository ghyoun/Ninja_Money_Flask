from flask import Flask, render_template, request, session, flash, redirect
import random
import datetime

app = Flask(__name__)
app.secret_key = "secretKey"


def coinFlip():
    if random.randrange(0, 2) == 1:
        return True
    else:
        return False

def logActivity(earned, place, earnOrLose):
    timeNow = datetime.datetime.now()
    if (place == 'farm' or place == 'cave' or place == 'house'):
        session['activity'].reverse()
        session['activity'].append(['earn', 'Earned %d from the %s! %s' % (earned, place, timeNow)])
        session['activity'].reverse()
    elif (place == 'casino'):
        if (earnOrLose == 'earned'):
            session['activity'].reverse()
            session['activity'].append(['earn', 'Earned %d from the %s! %s' % (earned, place, timeNow)])
            session['activity'].reverse()
        else:
            session['activity'].reverse()
            session['activity'].append(['lost', 'Entered a casino and lost %d gold... Ouch %s' % (earned, timeNow)])
            session['activity'].reverse()
    else:
        print "error"
@app.route('/')
def index():
    if session['gold'] == None:
        session['gold'] = 0
    if session['activity'] == None:
        session['activity'] = []
    return render_template('index.html', gold=session['gold'], activity=session['activity'])

@app.route('/process_money', methods=['POST'])
def money():
    buttonClicked = request.form['hidden']
    if (buttonClicked == 'farm'):
        earned = random.randrange(10, 21)
        session['gold'] += earned
        logActivity(earned, 'farm', 'earned')
    elif (buttonClicked == 'cave'):
        earned = random.randrange(5, 11)
        session['gold'] += earned
        logActivity(earned, 'cave', 'earned')
    elif (buttonClicked == 'house'):
        earned = random.randrange(2, 6)
        session['gold'] += earned
        logActivity(earned, 'house', 'earned')
    elif (buttonClicked == 'casino'):
        earned = random.randrange(0, 51)
        earn = coinFlip()
        if (earn == True):
            session['gold'] += earned
            logActivity(earned, 'casino', 'earned')
        else:
            session['gold'] -= earned
            logActivity(earned, 'casino', 'lost')
    return redirect('/')

@app.route('/clear', methods=['POST'])
def clear():
    session['gold'] = 0
    session['activity'] = []
    return redirect('/')


app.run(debug=True)
