#!/usr/bin/python

from __future__ import unicode_literals
from flask import Flask,request,Response
from threading import Thread,RLock
from contextlib import contextmanager
from github3 import login
import os
from qcloud_cos import *


app = Flask(__name__)
lock = RLock()
token = ''

@contextmanager
def status(sha):
    repo = login(token=token).repository('','')
    repo.create_status(sha,'pending')
    try:
        yield
        repo.create_status(sha,'success')
    except:
        repo.create_status(sha,'error')

def system(cmd):
    code = os.system(cmd)
    if code != 0:
        raise Exception('Error' + cmd)

def deploy(sha):
    with lock:
        with status(sha):
            if not os.path.isdir('web'):
                system('git clone https://github.com/lingmm/IssueBlog.git web')
            system('cd web && git pull && npm i && npm run build')
            os.chdir('web/dist')
            client = CosClient(,'','')
            for root,dirs,files in os.walk('.'):
                for f in files:
                    client.upload_file(UploadFileRequest('static',root[1:]+'/'+f,os.path.join(root,f)))


@app.route('/webhook',methods=['POST'])
def hook():
    event = request.headers.get('X-GitHub-Event',None)
    if event == 'push':
        sha = request.json['head_commit']['id']
        Thread(target=deploy,args=(sha,)).start()
    return Response(status=200)

if __name__=='__main__':
    app.run(port=80,host='0.0.0.0')
