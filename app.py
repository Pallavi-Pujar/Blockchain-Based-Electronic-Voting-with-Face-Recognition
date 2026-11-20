from flask import Flask, render_template, request, redirect, url_for, flash, session,jsonify
import mysql.connector as mq
from mysql.connector import Error
from markupsafe import Markup
from datetime import datetime
from werkzeug.utils import secure_filename
from datetime import datetime
from collections import Counter
import embeddings
import recognition
import blockchain
from collections import Counter
from flask_mail import Mail, Message
import random
import string
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
myblockchain = blockchain.Blockchain()


# Configure Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'bhavyajbhavya32@gmail.com'  # Replace with your email
app.config['MAIL_PASSWORD'] = 'tzummlhzagavibip'  # Replace with your email password
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

def dbconnection():
    con = mq.connect(host='localhost', database='facebvotingweb',user='root',password='root')
    return con

@app.route('/')
def home():
    return render_template('index.html', title='home')

@app.route('/loginpage')
def loginpage():
    return render_template('login.html',title='login')


@app.route('/registerpage')
def registerpage():
    con = dbconnection()
    cursor = con.cursor()
    cursor.execute("select * from constituencies")
    res = cursor.fetchall()
    return render_template('register.html',res=res)


@app.route('/addcandidatepage')
def addcandidatepage():
    con = dbconnection()
    cursor = con.cursor()
    cursor.execute("select * from constituencies")
    res = cursor.fetchall()
    return render_template('addcandidate.html',res=res)

@app.route('/addconstituencypage')
def addconstituencypage():
    return render_template('addcons.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['user']
        password = request.form['password']
        ltype = request.form['ltype']
        if ltype=='eauthority':
            con = dbconnection()
            cursor = con.cursor()
            cursor.execute("select * from eauthority where userid='{}' and pass='{}'".format(user,password))
            res = cursor.fetchall()
            if res==[]:
                message = Markup("<h3>Failed! Invalid User Id or Password</h3>")
                flash(message)
                return redirect(url_for('loginpage'))
            else:
                return redirect(url_for('addconstituencypage'))
        elif ltype=='voter':
            con = dbconnection()
            cursor = con.cursor()
            voterid = recognition.detectPerson()
            cursor.execute("select * from voters where voterid='{}' and pass='{}'".format(user,password))
            res = cursor.fetchall()
            if res==[]:
                message = Markup("<h3>Failed! Invalid voter id or Password</h3>")
                flash(message)
                return redirect(url_for('loginpage'))
            elif res[0][8]=="voted":
                message = Markup("<h3>Failed! You have already voted</h3>")
                flash(message)
                return redirect(url_for('loginpage'))
            elif res[0][8]=="notvoted":
                cid = res[0][6]
                cursor.execute("select * from constituencies where id={}".format(int(cid)))
                res2 = cursor.fetchall()
                if res2[0][2]=="Inactive":
                    message = Markup("<h3>Failed! voting has not yet stated to this constitution</h3>")
                    flash(message)
                    return redirect(url_for('loginpage'))
                elif voterid==res[0][5]:
                    print(res[0][0])
                    session['vid']=res[0][0]
                    return redirect(url_for('vviewcandidates',cid=res[0][6]))
                else:
                    message = Markup("<h3>Failed! Face and Entered Voterid did not match</h3>")
                    flash(message)
                    return redirect(url_for('loginpage'))



@app.route('/savecandidate', methods=['GET', 'POST'])
def savecandidate():
    if request.method == 'POST':
        name = request.form['name']
        party = request.form['party']
        cid = request.form['cid']
        uploaded_file = request.files['photo']
        if uploaded_file.filename != '':
            # Save the uploaded file to a specific folder
            filename = 'static/uploads/partyimages/' + uploaded_file.filename
            onlyfilename=uploaded_file.filename
            print(filename)
            uploaded_file.save(filename)
        con = dbconnection()
        cursor = con.cursor()
        cursor.execute("select * from candidates where cname='{}' and party='{}' and cid='{}'".format(name,party,int(cid)))
        res = cursor.fetchall()
        if res==[]:
            cursor.execute("insert into candidates(cname,party,symbol,cid)values('{}','{}','{}',{})".format(name,party,onlyfilename,cid))
            con.commit()
            con.close()
            message = Markup("<h3>Success! Candidate Added!</h3>")
            flash(message)
            return redirect(url_for('addcandidatepage'))
        else:
            message = Markup("<h3>Failed! Candidate Already Exists!</h3>")
            flash(message)
            return redirect(url_for('addcandidatepage'))

@app.route('/viewcandidatespage')
def viewcandidatespage():
    con = dbconnection()
    cursor = con.cursor()
    cursor.execute("select * from candidates inner join constituencies on candidates.cid=constituencies.id")
    res = cursor.fetchall()
    if res==[]:
        message = Markup("<h3>Failed! Details not found</h3>")
        flash(message)
        return render_template('viewcandidates.html', title='candidates')
    else:
        return render_template('viewcandidates.html', title='candidates',res=res)

@app.route('/saveconstituency', methods=['GET', 'POST'])
def saveconstituency():
    if request.method == 'POST':
        consname = request.form['consname']
        status = 'Inactive'
        con = dbconnection()
        cursor = con.cursor()
        cursor.execute("select * from constituencies where consname='{}'".format(consname))
        res = cursor.fetchall()
        if res==[]:
                cursor.execute("insert into constituencies(consname,status)values('{}','{}')".format(consname,status))
                con.commit()
                con.close()
                message = Markup("<h3>Success! Details Added!</h3>")
                flash(message)
                return redirect(url_for('addconstituencypage'))
        else:
            message = Markup("<h3>Failed! Constitution already exists!</h3>")
            flash(message)
            return redirect(url_for('addconstituencypage'))


@app.route('/viewconstituenciespage')
def viewconstituenciespage():
    con = dbconnection()
    cursor = con.cursor()
    cursor.execute("select * from constituencies")
    res = cursor.fetchall()
    if res==[]:
        message = Markup("<h3>Failed! Details not found</h3>")
        flash(message)
        return render_template('viewcons.html', title='constitutions')
    else:
        return render_template('viewcons.html', title='constitutions',res=res)
    


    
@app.route('/deactivate')
def deactivate():
    id =request.args.get('id')
    status = 'Inactive'
    con = dbconnection()
    cursor = con.cursor()
    cursor.execute("update constituencies set status='{}' where id={}".format(status,int(id)))
    con.commit()
    con.close()
    message = Markup("<h3>Success! constituency Deactivated</h3>")
    flash(message)
    return redirect(url_for('viewconstituenciespage'))

@app.route('/activate')
def activate():
    print("active")
    id =request.args.get('id')
    status = 'Active'
    con = dbconnection()
    cursor = con.cursor()
    cursor.execute("update constituencies set status='{}' where id={}".format(status,int(id)))
    con.commit()
    con.close()
    message = Markup("<h3>Success! constituency Activated</h3>")
    flash(message)
    return redirect(url_for('viewconstituenciespage'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        aadharid = request.form['aadharid']
        voterid = request.form['voterid']
        gender = request.form['gender']
        cid = request.form['cid']
        password = request.form['password']
        status="notvoted"
        con = dbconnection()
        cursor = con.cursor()
        cursor.execute("select * from voters where aadharid='{}' or voterid='{}'".format(aadharid,voterid))
        res = cursor.fetchall()
        if res==[]:
            try:
                embeddings.trainPerson(voterid,aadharid)
                cursor.execute("insert into voters(name,phone,gender,aadharid,voterid,cid,pass,status)values('{}','{}','{}','{}','{}',{},'{}','{}')".format(name,phone,gender,aadharid,voterid,int(cid),password,status))
                con.commit()
                con.close()
                message = Markup("<h3>Registration Success</h3>")
                flash(message)
                return redirect(url_for('registerpage'))
            except Exception as e:
                print("An error occurred:", e)
                message = Markup("<h3Could not complete registration</h3>")
                flash(message)
                return redirect(url_for('registerpage'))
        else:
            message = Markup("<h3>Failed! aadharid or voterid already exists</h3>")
            flash(message)
            return redirect(url_for('registerpage'))
    
@app.route('/vviewcandidates/<int:cid>')
def vviewcandidates(cid):
    con = dbconnection()
    cursor = con.cursor()
    cursor.execute("select * from candidates inner join constituencies on candidates.cid=constituencies.id where candidates.cid={}".format(int(cid)))
    res = cursor.fetchall()
    if res==[]:
        message = Markup("<h3>Failed! Details not found</h3>")
        flash(message)
        return render_template('vviewcandidates.html', title='candidates')
    else:
        return render_template('vviewcandidates.html', title='candidates',res=res)

@app.route('/savemyvote')
def savemyvote():
    #print("hello")
    cid =request.args.get('id')
    status = "voted"
    vid = session['vid']
    con = dbconnection()
    cursor = con.cursor()
    cursor.execute("update voters set status='{}' where id={}".format(status,int(vid)))
    con.commit()
    myblockchain.add_block(cid, "yes", vid)
    blocks = myblockchain.get_blocks()
    for block in blocks:
        print(block)
    message = Markup("<h3>Sucess! Thank you for voting your vote is safe in blockchain</h3>")
    flash(message)
    return redirect(url_for('loginpage'))

@app.route('/viewvotecountspage')
def viewvotecountspage():
    con = dbconnection()
    cursor = con.cursor()
    cursor.execute("select * from candidates")
    res = cursor.fetchall()

    votes = []
    blocks = myblockchain.get_blocks()

    # Collect votes from blocks
    for block in blocks:
        if block[2] is not None:  # Ensure block[2] is not None
            votes.append(block[2])

    counter = Counter(votes)
    unique_ids = list(counter.keys())
    frequencies = list(counter.values())
    finalresult = []

    for number, frequency in zip(unique_ids, frequencies):
        if number is not None:  # Ensure number is not None before processing
            cursor.execute("select * from candidates inner join constituencies on candidates.cid=constituencies.id where candidates.id={}".format(int(number)))
            res1 = cursor.fetchall()
            for sublist in res1:
                modified_sublist = list(sublist)
                modified_sublist.append(str(frequency))
                finalresult.append(modified_sublist)

    print(finalresult)
    return render_template('viewvotecount.html', title='votes', res=finalresult)


@app.route('/search_cons', methods=['POST'])
def search_cons():
    data = request.get_json()
    search_term = data['searchTerm'].lower()  # Get the search term from the request
    con = dbconnection()
    cursor = con.cursor()
    
    # Query to filter candidates based on constituency name
    cursor.execute("""
        SELECT candidates.id AS cid, candidates.cname AS candidate_name, candidates.party AS party, 
               constituencies.consname AS constituency_name 
        FROM candidates 
        INNER JOIN constituencies ON candidates.cid = constituencies.id 
        WHERE LOWER(constituencies.consname) LIKE %s
    """, ('%' + search_term + '%',))
    
    results = cursor.fetchall()
    final_result = []
    
    # Process results to include vote counts
    votes = [block[2] for block in myblockchain.get_blocks()]  # Extract candidate IDs from blockchain votes
    counter = Counter(votes)
    
    for candidate in results:
        cid = candidate[0]
        candidate_name = candidate[1]  # Adjust based on the selected fields
        party = candidate[2]
        constituency_name = candidate[3]
        
        # Get vote count from the counter
        vote_count = counter.get(str(candidate[0]), 0)  # Make sure you pass the correct ID for counting
        
        # Add the required data to the final result
        final_result.append([candidate_name, party, constituency_name, str(vote_count)])

    return jsonify(final_result)  # Return results as JSON

# OTP storage
otp_store = {}

# Route to send OTP
@app.route('/send_otp', methods=['POST'])
def send_otp():
    data = request.get_json()
    email = data.get('email')

    # Generate OTP
    otp = ''.join(random.choices(string.digits, k=6))
    otp_store[email] = {'otp': otp, 'expiry': time.time() + 300}  # OTP expires in 5 minutes
    session[email]=otp

    # Send OTP email
    msg = Message('Your OTP Code', sender='your_email@gmail.com', recipients=[email])
    msg.body = f'Your OTP code is {otp}'
    try:
        mail.send(msg)
        return jsonify({"status": "success"}), 200
    except Exception as e:
        print(str(e))
        return jsonify({"status": "fail"}), 400

# Route to verify OTP
@app.route('/verify_otp', methods=['POST'])
def verify_otp():
    data = request.get_json()
    otp = data.get('otp')
    email = data.get('email')  # Get email from form, or you can pass via the API as well
    otp_store = session[email]
    if email in otp_store:

        return jsonify({"status": "success"}), 200
    else:
        return jsonify({"status": "fail"}), 400

@app.teardown_appcontext
def shutdown_session(exception=None):
    myblockchain.save_chain()  # Save the blockchain data when the app context is torn down


                



if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=5000)
