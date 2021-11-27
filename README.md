


# Welcome to AUB COVAX

# A platform built with python django and Android studio




<<<<<<<DEMO VIDEO: http://youtu.be/ayRH3wVqUS4 >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>








 the requirements for the project are the following

1- INSTALL PYTHON 

www.python.org ->Downloads->Python 3.6.4-Download->(other executable installer that is compatible with your platform)

Save the installer on your hard Disk (C:\ drive or any other location)
Double click to install

Checked: Install launcher for all users (recommended)

Check: Add Python 3.6.4 to PATH (The version you chose)

Click on: Install Now
DONE………………………

2-INSTALL PIP:

python3 -m pip install --upgrade pip

3- INSTALL DJANGO

pip3 install django

4- Go to project inside terminal (cd into project AUBCOVAX)

5- install the appropriate libraries:

pip3 install lxml
pip3 install docx-mailmerge
pip3 install docx2pdf

6-run the following commands: 

#to load project
python3 manage.py migrate 

#to runserver
python3 manage.py runserver 0.0.0.0:8000





On the android studio side:

1-open project AUBCOVAXAPP

2-Choose the appropriate emulator

3-in Mainactivity.java:
    in String url: write  //"http://10.0.2.2:8000" if you want a loopback on emulator
                   write "yourIP and PORTNAME" if you want it on the local network on another device

4 - do the same in MyWebViewClient.java file with the variable "hostname"


5-Enjoy!!



P.S. You might run into some permission issues for generating and sending
a certificate upon the second dose confirmation

to fix that, go to the django project, in the Certificates file, allow write and read
as permissions by going into
: Get info in MAC OSX
: properties > Security > Full Control on PC





