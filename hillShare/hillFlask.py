from jsonpickle import encode
from flask import Flask
from flask import abort, redirect, url_for
from flask import request
from flask import render_template
from flask import session
import logging
from flask import json
from logging.handlers import RotatingFileHandler
from logging import Formatter
from userdao import UserDao
from user import User
from HillshareGroup import Group
from HillshareGroupDao import GroupDao
from HillshareMessage import Message
from HillshareMessageDao import MessageDao
from HillshareEventDao import EventDao
from HillshareEvent import Event
from flask import jsonify
from flask import Response

app = Flask(__name__)

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['POST', 'GET'])    
def login():    
    error = None    
    if (request.method =='POST'):
           
        if('userid' in request.form and 'password' in  request.form):
             
            if isValid(request.form['userid'],request.form['password']):
                                                                    
                session['userid']=request.form['userid']
                return redirect(url_for('home'))
            else:
            
                return render_template('login.html', error=error)
        else:
                                   
            return render_template('login.html', error=error)
                        
            
    elif(request.method=='GET'):
                
        return render_template('login.html', error=error)
	 

                             
                             
def isValid(userid, password):
    dao = UserDao()
    user = dao.selectByUserid(userid)
    
                
    if (user is not None) and (userid == user.userid) and (password == user.password):
        session['user']=encode(user) # use an encoder to convert user to a JSON object for session
        return True
    else:
        return False
def taken(name):
    gdao=GroupDao()
    names=gdao.selectByName(name)
    if names is None:
        return False
    else:
        return True

@app.route('/home', methods=['POST', 'GET'])
def home():
    dao=UserDao()
    user=dao.selectByUserid(session['userid'])
    groups=dao.returnUserList(user.userid)
    gdao=GroupDao()
    gro=[]
    for group in groups:
        gro.append(gdao.selectByName(group))
        
    
    if(request.method=='POST'):
        if("view" in request.form):
            
            session["grouptoview"]=request.form['view']
            return redirect(url_for("view"))
        else:
            return render_template('home.html', **locals())
                
    elif(request.method=='GET'):
        return render_template('home.html', **locals())

@app.route('/table', methods=['POST', 'GET'])
def table():
    daomess=MessageDao(session['grouptoview'])
    messages=daomess.selectAll()
    messages.reverse()
    result=json.dumps({"data" : fakejson(messages)})
    app.logger.debug(json.dumps({"data" : fakejson(messages)}))
    app.logger.debug(Response(result,mimetype='application/json'))
    
    return Response(result,mimetype='application/json')

def fakejson(data):
    temp=[]
    for message in data:
        var=message.JJ()
        
        temp.append(var)
        
    return temp
    


@app.route('/groupsearch',methods=['POST','GET'])
def groupsearch():
    userid=session['userid']
    userdao=UserDao()
    user=userdao.selectByUserid(userid)        
    allg=GroupDao()
    groups=allg.selectAll()
    if (request.method=='POST'):
        return render_template('groupsearchresults.html', **locals())    
    elif(request.method=='GET'):
        return render_template('groupsearchresults.html', **locals())
            

    
    
@app.route('/request1',methods=['POST','GET'])
def request1():
    
    groupname = request.args.get('name')
    daomess=MessageDao(groupname)
    mess=Message('System', session['userid']+' would like to join the group','/static/join_icon.png')
    daomess.insert(mess)
    return redirect(url_for("groupsearch"))
    
    
@app.route('/view', methods=['POST', 'GET'])
def view():
    error=None
    userid=session['userid']
    userdao=UserDao()
    user=userdao.selectByUserid(userid)
    gdao=GroupDao()               
    gname=session['grouptoview']
    tgname=gname
    groupname=gdao.selectByName(gname) 
    daomess=MessageDao(gname)
    messages=daomess.selectAll()
    messages.reverse()
    data=messages
    if (request.method == 'POST'):
        
        if(request.form["submitnewmessage"]=="Add New Message"):
            m=Message(session['userid'],request.form["textvalue"],user.profPic)
            daomess.insert(m)
            messages=daomess.selectAll()
            return redirect(url_for("view"))
        
        elif(request.form["submitnewmessage"]== "Add New User"):
            app.logger.debug("HERe")        
            uta=request.form["newUser"]
            if(not nottaken2(uta)):
                ouserdao=UserDao()
                ouserdao.addMember(uta,gname)
                gdao.addMember(gname,uta)
                return redirect(url_for("view"))
            else:
                return redirect(url_for("view"))
        elif(request.form["submitnewmessage"]=="Create Event"):
            eventname=request.form["eventname"]
            eventdes=request.form["eventdescription"]
            eventstart=request.form["starttime"]
            eventend=request.form["endtime"]
            tempst=eventstart.split("T")
            tempen=eventend.split("T")
            datest=tempst[0]
            dateen=tempst[0]
            tempdayst=datest.split("-")
            yearst=tempdayst[0]
            monthst=tempdayst[1]
            dayst=tempdayst[2]
            tempdayen=dateen.split("-")
            yearen=tempdayen[0]
            monthen=tempdayen[1]
            dayen=tempdayen[2]           
            timest=tempst[1]
            timeen=tempen[1]
            newEvent = Event( dayst, monthst, yearst, dayen, monthen, yearen, timest, timeen, eventname, eventdes, gname,"")
            dao = EventDao()
            dao.insertEvent(newEvent)
            return redirect(url_for("view"))
                    
            
        else:
            return redirect(url_for("view"))
    elif (request.method == 'GET'):
        return render_template('view.html', **locals())
            
        
@app.route('/lookup', methods=['POST', 'GET'])
def events():
    userid=session['userid']
    userdao=UserDao()
    user=userdao.selectByUserid(userid)        
    dao=EventDao()
    dao.expire()
    events=dao.selectAll()
    if(request.method=='POST'):
        return render_template('events.html', **locals())
    elif(request.method=='GET'):
        return render_template('events.html', **locals())
            
            
    
@app.route('/create', methods=['POST', 'GET'])
def create():
    error=None
    userid=session['userid']
    userdao=UserDao()
    user=userdao.selectByUserid(userid)
    
                   
    if(request.method=='POST'):
        if(request.form["submitnewgroup"]=="Create Group"):
            name=request.form['name']
            if(not taken(name)):
               us=UserDao()
               us.addMember(session['userid'],name)
               descr=request.form['description']
               mess=request.form['mess']
               gdao=GroupDao()
               newg=Group(name,descr,session['userid'])
               gdao.insert(newg)
               mdao=MessageDao(name)
               m=Message(session['userid'],mess,user.profPic)
               mdao.insert(m)  
               return redirect(url_for('home'))
           
            else:
               return render_template('creategroup.html', **locals())
    elif(request.method=='GET'):
        return render_template('creategroup.html', **locals())
                    
               
@app.route('/new', methods=['POST', 'GET'])
def new():
    error = None
    
    #Wapp.logger.debug("password1" in request.form)
    if (request.method == 'POST'):
        if request.form['submitnew']=='submit':            
            if request.form['userid1']is not None and request.form['password1']is not None:
                if nottaken(request.form['userid1'],request.form['password1']):                    
                    userid=request.form['userid1']
                    password=request.form['password1']
                    em=request.form['emailaddress']
                    pic=request.form.get('pic')
                    dao= UserDao()
                    us=User(userid,password,em,pic,'')
                    dao.insert(us)
                    return redirect(url_for('login'))
                else:
                    return render_template('new.html', error=error)
                        
           # the code below is executed if the request method
            # was GET or the credentials were invalid
    elif (request.method=='GET'):
        return render_template('new.html', error=error)
def nottaken2(userid):
        #app.logger.debug(userid)
        dao= UserDao()
        #app.logger.debug(userid)
        use=dao.selectByUserid(userid)
        if use is None:
            return True
        else:
            return False
                            
def nottaken(userid,password):
    #app.logger.debug(userid)
    dao= UserDao()
    #app.logger.debug(userid)
    use=dao.selectByUserid(userid)
    if use is None:
        return True
    else:
        return False
if __name__ == "__main__":
    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
    #    context = ('ssl.cert', 'ssl.key')
    handler = RotatingFileHandler('output.log', maxBytes=10000, backupCount=1)
    handler.setFormatter(Formatter("[%(filename)s:%(lineno)s - %(funcName)10s() ] %(message)s"))
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.DEBUG)
    app.run(host='0.0.0.0')
