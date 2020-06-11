短網址:https://reurl.cc/z8ElAN

前言
本專案利用AWS Elastic Beanstalk佈建Django專案。

前置作業
AWS Free Tier(一年期的免費帳號)
Pycharm
Anaconda
Python 3.7
pip
virtualenv
awsebcli


1.於Pycharm建立一個Django專案<br />
![image](https://gitlab.com/hpsh31323/picture/-/raw/master/Creat%20Django%20Project%20On%20AWS/creat_django_project.png)

2.Terminal: **python manage.py migrate**

此時的目錄結構<br />
![image](https://gitlab.com/hpsh31323/picture/-/raw/master/Creat%20Django%20Project%20On%20AWS/divlist1.png)

3.執行Django專案<br />
Terminal: **python manage.py runserver**

執行後會看到Starting development server at http://127.0.0.1:8000/的訊息<br />
進入http://127.0.0.1:8000/ 網頁後會看到django預設畫面<br />
![image](https://gitlab.com/hpsh31323/picture/-/raw/master/Creat%20Django%20Project%20On%20AWS/django.png)

4.保存相依套件<br />
Terminal: **pip freeze > requirements.txt**<br />
後續AWS Elastic Beanstalk會依照requirements.txt的檔案內容來判斷執行應用程式的EC2 Instance應該需安裝哪些套件。

5.建立 .ebextensions 的目錄<br />
Terminal:**mkdir .ebextensions**

6.在.ebextensions目錄下建立配置的檔案django.config<br />
Terminal:**touch django.config**
