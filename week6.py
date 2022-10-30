from flask import Flask,request,render_template,redirect,session,url_for
import mysql.connector

app = Flask(__name__,
    static_folder="static",
    static_url_path="/")

#設定 session 密鑰
app.secret_key='tian12345'

# mysql.connector 引入方式
new = mysql.connector.connect(
  host="localhost",
  user="root",
  password="tian0426",
  database="signin" 
)
#mycursor = new.cursor()
# mycursor.execute("create table message(content varchar(255))")
# mycursor.execute("show tables")
# mycursor.execute("SELECT * FROM message")
# myresult = mycursor.fetchall() 
# for x in myresult:  
#     print (x)

#建立database,table

# index.route - index.html
@app.route('/')
def index():
    return render_template("index.html")

#index.html - signup.route
@app.route('/signup',methods=['POST'])
def signup():
    #取得要求物件，連線到memeber，撈出資料庫 username, password欄位資料並同時符合user的值（代表資料庫內已有此組帳號）
    name = request.form['name']
    user = request.form['username']
    psw = request.form['password']
    #資料庫-撈取對應值後執行sql，並利用fetchall回傳值
    #execute()-執行  rowcount()-資料筆數 commit()-提交資料到資料庫
    mycursor = new.cursor()
    sql='SELECT username, password FROM member WHERE username = %s' %(user)
    mycursor.execute(sql)
    myresult = mycursor.fetchall() 
    # for x in myresult:     
    if (mycursor.rowcount != 0) :
        return redirect("http://127.0.0.1:3000/error?message=帳號已經被註冊")
    else:
        mycursor = new.cursor()
        sql2='INSERT INTO member(name, username, password) VALUES(%s, %s, %s)'
        val=(name, user, psw)
        mycursor.execute(sql2, val)
        new.commit()
        return redirect('/')

#註冊後回到首頁 #index.html - signin.route
@app.route('/signin', methods =['POST'])
def signin():
    #取得要求物件
    user = request.form['username']
    psw = request.form['password']
    #紀錄使用者管理
    session["username"]= user
    session["password"]= psw
    #資料庫-取得name, username, password三項欄位，username, password與要求物件取得的值相同，代表輸入正確帳號密碼
    #執行並取出值
    mycursor = new.cursor()
    sql='SELECT name, username, password FROM member WHERE username = %s and password = %s' % (user,psw)
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    # for x in myresult:
    # Tuple 去取值 myresult[0][0]=name /myresult[0][1]=user/ myresult[0][2]=psw
    #如果筆數為1，代表帳密輸入正確。
    if  mycursor.rowcount!=0 and myresult[0][1] == user and myresult[0][2] == psw:
        name = request.args.get("name","")
        #使用者紀錄等於資料庫name的值
        session['name'] = myresult[0][0]
        #使用者紀錄保持登入狀態
        session['enter'] = 'open'
        return redirect(url_for("member")) 
    else:        
        return redirect("http://127.0.0.1:3000/error?message=帳號、或密碼輸入錯誤") 

#signin.route -  member.route
@app.route('/member')
def member():
    #假設使用者紀錄保持登入狀況，會導向前端，並取出name值，印在畫面上
    if "open" == session['enter']:
        name = session['name'] 
        return render_template("member.html",name = name)
    else:
        return redirect('/')
    #沒有使用者紀錄，回到首頁

@app.route('/error')
def error():
    data = request.args.get('message',"")
    return render_template("error.html", data = data)
    
@app.route('/signout',)
def signout():
     session['enter'] = 'close'
     return redirect('/')

#在資料庫中加入留言欄位

# @app.route('/message',methods=['POST'])
# def message():

#     content = request.form['content']
#     mycursor = new.cursor()
#     sql3='INSERT INTO message(content) VALUES(%s)' %(content)
#     mycursor.execute(sql3)
#     new.commit()
#     # session['content']=content
#     name = request.args.get('name','')
#     content = request.arg.get('content','')
#     return render_template('member.html',name=name, content=content)
    
    # session["message"]= text
    # session["name"] = name
    # return render_template('member.html', (name,message)==(name,message))

if __name__ == "__main__":
    app.run(port=3000,debug=True)

