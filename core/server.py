# 导入Flask类
from flask import Flask,request,render_template
from colorama import init,Fore,Back,Style
from time import sleep
from requests import JSONDecodeError, session
import json,colorama,datetime,os,shutil
import threading
from threading import Lock
lock = Lock()
# 实例化，可视为固定格式
app = Flask(__name__,static_url_path='/static')

tokens = ['token1','1234567890abcdef']
tokendb = []

def raise_fault(msg):
    print(Fore.RED+msg+Style.RESET_ALL)
    exit(0)

def clears():
    global tokendb,__config_paint_time
    while True:
        tokendb=[]
        sleep(__config_paint_time)

def rendering_daemon():
    global __config_backup_time,__config_flush_time
    while True:
        print("rander-")
        # print(datetime.datetime.now().strftime("%Y%m%d%H%M%S"))

        # os.remove('./data/board_rendered.txt')

        #? file render.

        lock.acquire()
        tf = open("./data/board_latest.txt","r")
        tfw = open("./data/board_rendered.txt","w")
        
        tmp = []
        for i in range(__config_max_x):
            tmp.append([])
            for j in range(__config_max_y):
                tmp[i].append('fff')
        
        while True:
            st = tf.readline(9)
            if st == '':break

            # print(st)
            x = st[0]+st[1]+st[2]
            y = st[3]+st[4]+st[5]
            colr = st[6]
            colg = st[7]
            colb = st[8]
            x = int(x,16)
            y = int(y,16)
            colr = int(colr,16)
            colg = int(colg,16)
            colb = int(colb,16)
            tmp[x][y]=st[6:9]
            # print(x,y,st[6:9])

        for j in range(__config_max_y):
            for i in range(__config_max_x):
                # print(tmp[i][j],end='')
                tfw.write(tmp[i][j])
        tfw.close()
        lock.release()

        sleep(__config_flush_time)



def copying_daemon():
    while True:
        lock.acquire()
        shutil.copyfile("./data/board_rendered.txt","./data/"+datetime.datetime.now().strftime("%Y%m%d%H%M%S")+".txt")
        lock.release()
        sleep(__config_backup_time)



def pre_load_config():
    global __config
    lock.acquire()
    try:
        f = open('/data/.config','r')
    except FileNotFoundError:
        try:
            f = open('.tmpconfigremoveme','r')
        except FileNotFoundError:
            raise_fault("ERROR:config file not found!")
    lock.release()

    try:
        __config = json.loads(f.read())
    except json.decoder.JSONDecodeError:
        raise_fault("ERROR:decode error!")

def load_config():
    pre_load_config()
    global __config_max_x,__config_max_y,__config_backup_time,__config_paint_time,__config_flush_time
    try:
        __config_max_x = __config['map']['x']
        __config_max_y = __config['map']['y']
        __config_backup_time = __config['backup']
        __config_paint_time = __config['painttime']
        __config_flush_time = __config['flushtime']
    except KeyError:
        raise_fault("ERROR:some config don't exist!")

def __checktoken(token):
    if token in tokens:
        return "1"
    return "0"

@app.route('/paint',methods=['GET', 'POST'])
def paint():
    if request.method == "GET":
        paras = request.args
    elif request.method == "POST":
        paras = request.form
    paras = paras.to_dict()

    try:
        token = paras['token']
        x     = paras['x']
        y     = paras['y']
        col   = paras['col']

        status = 1
        #? check token
        if status==1 :
            if token in tokendb:
                status=-1
            if not token in tokens :
                status=0
        
        #? check x
        if status==1 :
            try:
                if 0<=int(x) and int(x)<__config_max_x:
                    pass
                else:
                    status=0
            except ValueError:
                status=0

        #? check y
        if status==1 :
            try:
                if 0<=int(y) and int(y)<__config_max_y:
                    pass
                else:
                    status=0
            except ValueError:
                status=0
        
        #? check token
        if status==1 :
            try:
                if len(col)!=3:
                    status=0
                if 0>=int(col,16) or 4096<=int(col,16):
                    status=0
            except ValueError:
                status=0

        if status==1:
            lock.acquire()
            #! CHANGE IT INTO PRODUCT
            open('./data/board_latest.txt','a').write("%03x%03x"%(int(x),int(y))+col)
            #! PRODUCT
            #? open('/data/board_latest.txt','a').write("%03x%03x"%(int(x),int(y))+col)
            lock.release()

            # tokendb.append(token)


        # print(hex(int(x)),hex(int(y)))
        # open(sys.path[0]+'/data/board_latest.txt','a').write(str({"token":token,"pos":(x,y),"col":col}))

    except KeyError:
        return str({"code":-1,"desc":"value incorrect"})
    return str({"code":0,"success":status})


@app.route('/checktoken',methods=['GET', 'POST'])
def checktoken():
    if request.method == "GET":
        paras = request.args
    elif request.method == "POST":
        paras = request.form
    paras = paras.to_dict()

    try:
        st = __checktoken(paras['token'])
        return str({"code":0,"status":st})
    except KeyError:
        return str({"code":-1,"desc":"value incorrect"})

@app.route('/board',methods=['GET', 'POST'])
def board():
    lock.acquire()
    f = open('./data/board_rendered.txt','r').read()
    lock.release()
    return f

@app.route('/',methods=['GET', 'POST'])
def serve():
    return render_template('./index.html')

@app.errorhandler(404)
def reactwhen404(error):
    return render_template('./404.html'), 404

if __name__ == '__main__':
    load_config()

    copyingdaemon = threading.Thread(target=copying_daemon)
    copyingdaemon.setDaemon(True)
    copyingdaemon.start()

    flushingdaemon = threading.Thread(target=rendering_daemon)
    flushingdaemon.setDaemon(True)
    flushingdaemon.start()

    sessionclean = threading.Thread(target=clears)
    sessionclean.setDaemon(True)
    sessionclean.start()

    app.run(host="0.0.0.0", port=5000)
    # copying_daemon()