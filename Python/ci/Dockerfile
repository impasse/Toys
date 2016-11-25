 FROM node:6
 
 EXPOSE 80
 
 RUN apt-get -y update\
   && apt-get -y install git python python-pip
 RUN pip install flask qcloud_cos github3.py
 
 COPY hook.py /srv/hook.py
 RUN chmod +x /srv/hook.py
 
 ENTRYPOINT ['/srv/hook.py']
