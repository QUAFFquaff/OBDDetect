# OBDDetect
driving detection and producting

# Environment Setting:
##  Hardware
* 1. Install the Freematics device to car.
* 2. To pair the Freematics with RPi, then run the following command in a terminal:
****sudo rfcomm bind 0 24:0A:C4:06:50:2A 2****
This will bind the Freematics device to /dev/rfcomm0 on channel 2.      
Afterwards, /dev/rfcomm0 can be read like any serial device.
(this step can be run with shell script when pi startup)  
* 3. Start OBD run the EventDetect.py

## Software
****required**** python3.5
* 1.install python packages needed in program:
  - xlrd
  - xlwd
  - xlutils
  - pip install --user numpy
  - pip install --user scipy or sudo apt-get install python3-scipy
  - pip install --user pandas
  - pip install --user joblib
  - pip install --user -U scikit-learn
  - pip install --user pymysql
  - pip install --user gensim
  - pip install --user stop_words
  - pip install --user nltk
  - pip install --user fuzzywuzzy
 
* 2.startup bluetooth
  - set up shell script for bluetooth    
    run chmod 777 testboot.sh  
    add command to rc.local at /etc/rc.local  
  - ****Or**** copy shell script to /etc/init.d  
	  run sudo update-rc.d script defaults 95  
	  sudo systemctl enable bluetoothconn.service  

# Development Knowledge
  - Arduino ****Install lib****   
    https://www.arduino.cc/en/Guide/Libraries?setlang=cn  
  
  - Rasp pi ****connect bluetooth****  
    https://blog.csdn.net/bona020/article/details/52141363  
  
  - Excel ****analyze data****    
    https://zhidao.baidu.com/question/203882457.html  
  
  - context.get ****counter in java script****    
    https://blog.csdn.net/geek_monkey/article/details/80751284

  - Node-red ****write function****    
    https://nodered.org/docs/writing-functions  
  
  - freematics ****data logger****  
    https://freematics.com/pages/hub/freematics-data-logging-format/  

  - freematics ****library****  
    https://freematics.com/pages/products/freematics-one-plus/  

Team Name:

* ****Quaff****

* ****Daben****
