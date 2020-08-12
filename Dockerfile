# Container for developing in MongoDb and Python 3 at Holberton School
FROM holbertonschool/ubuntu-1404-python3

MAINTAINER Guillaume Salva <guillaume@holbertonschool.com>

RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 2930ADAE8CAF5059EE73BB4B58712A2291FA4AD5
RUN echo "deb [ arch=amd64 ] http://repo.mongodb.org/apt/ubuntu trusty/mongodb-org/3.6 multiverse" > /etc/apt/sources.list.d/mongodb-org-3.6.list


RUN apt-get update

# install google chrome
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN dpkg -i google-chrome-stable_current_amd64.deb; apt-get -fy install

# install chromedriver
RUN apt-get install -yqq unzip
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

# set display port to avoid crash
ENV DISPLAY=:99

# install selenium
RUN pip3 install selenium==3.8.0

# create directory for mongodb 
RUN mkdir -p /data/db

# install mongodb
RUN apt-get install -y mongodb-org

# install and initialize mongo
RUN pip3 install pymongo

# install all needed libraries
RUN pip3 install bs4
RUN pip3 install urllib
RUN sudo apt-get install python3-pandas
RUN pip3 install re
RUN pip3 install pytesseract
RUN pip3 install pdf2image
RUN pip3 install pillow
RUN pip3 install django-mongodb-engine
RUN pip3 install html5lib


ADD init.d-mongod /etc/init.d/mongod
RUN chmod u+x /etc/init.d/mongod

ADD run.sh /tmp/run.sh
RUN chmod u+x /tmp/run.sh

# start run!
CMD ["./tmp/run.sh"]