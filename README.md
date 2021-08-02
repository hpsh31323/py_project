
前言<br />
本專案利用AWS Elastic Beanstalk佈建Django專案。

前置作業:<br />
AWS Free Tier(一年期的免費帳號)<br />
Pycharm<br />
Anaconda<br />
Python 3.7<br />
pip<br />
virtualenv<br />
awsebcli<br />
awscli<br />

**A.Django專案建置到部署**

1.於Pycharm建立一個Django專案<br />
![image](https://gitlab.com/hpsh31323/picture/-/raw/master/Creat%20Django%20Project%20On%20AWS/creat_django_project.png)

2.
> python manage.py migrate

此時的目錄結構<br />
![image](https://gitlab.com/hpsh31323/picture/-/raw/master/Creat%20Django%20Project%20On%20AWS/divlist1.png)

3.執行Django專案<br />

> python manage.py runserver

執行後會看到Starting development server at http://127.0.0.1:8000/的訊息<br />
進入http://127.0.0.1:8000/ 網頁後會看到django預設畫面<br />
![image](https://gitlab.com/hpsh31323/picture/-/raw/master/Creat%20Django%20Project%20On%20AWS/django.png)

4.保存相依套件<br />

> pip freeze > requirements.txt

後續AWS Elastic Beanstalk會依照**requirements.txt**的檔案內容來判斷執行應用程式的EC2 Instance應該需安裝哪些套件。

5.建立 **.ebextensions** 的目錄<br />

> mkdir .ebextensions

6.在**.ebextensions**目錄下建立配置的檔案django.config<br />

> touch django.config

7.在**django.config**中寫入以下指令<br />
注意：依AWS平台版本不同，WSGIPath會有不同寫法，如：ebdjango/wsgi.py
> option_settings:\
&nbsp;&nbsp;&nbsp;&nbsp;aws:elasticbeanstalk:container:python:\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;WSGIPath: ebdjango.wsgi.py

8.建立AWS IAM帳號並開啟以下三個權限後下載包含**AWS Access Key ID**和**AWS Secret Access Key**的**CSV檔**
- AWSElasticBeanstalkFullAccess
- AmazonEC2FullAccess
- AmazonS3FullAccess

9.安裝awsebcli與awscli
> pip install awsebcli
pip install awscli

10.AWS ebcli登入<br />
此時會要求輸**入AWS Access Key ID**和**AWS Secret Access Key**
> aws configure

11.初始化EB CLI 儲存庫
> eb init -p python-3.7 django-project

11.5 設定**.elasticbeanstalk**底下的**config.yml**中的服務區域
> default_region: <你的服務區域>

12.建立部署環境
> eb create < your_env_name>-env

13.查看部署環境並複製**CNAME**的訊息，它代表你的網域位置。
> eb status

14.配置domain<br />
將從**CNAME**複製下來的訊息貼到專案中的**settings.py**檔內
> ALLOWED_HOSTS = ['CNAME網域訊息', '127.0.0.1:8000']

15.部署
> eb deploy

看到Environment update completed successfully表示部署成功！

**B.配置靜態檔案(css/js/image...)**

1.在AWS S3上新增**Bucket** (服務區域ex:us-west-2 )
> aws s3api create-bucket \
>   --acl public-read \
>   --region <你的服務區域> \
>   --create-bucket-configuration LocationConstraint=<你的服務區域> \
>   --bucket < Your bucket name> \

  
  執行後會出現以下訊息
  > {\
    "Location": "http:// < Your bucket name>.s3.amazonaws.com/"\
}

2.將新增的**Bucket URL**設定到環境中

> eb setenv <Your env name> STATIC_URL=https://<Your bucket name>.s3.amazonaws.com/

3.設定Bucket Policy
> aws s3api put-bucket-policy \
&nbsp;&nbsp;&nbsp;--bucket <Your bucket name> \
&nbsp;&nbsp;&nbsp;--policy '{\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"Version": "2012-10-17",\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"Statement": [\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"Sid": "PublicReadForGetBucketObjects",\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"Effect": "Allow",\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"Principal": "*",\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"Action": "s3:GetObject",\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"Resource": "arn:aws:s3:::<Your bucket name>/*"\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;}\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;]\
&nbsp;}'

4.在**settings.py**中增加下方程式碼
> STATIC_URL = os.getenv('STATIC_URL', '/static/')
> STATIC_ROOT = os.path.join(BASE_DIR, 'static')

注意:**STATIC_ROOT**用於正式環境，如在本地開發環境則使用下方程式碼，並須將**STATIC_ROOT**先註解掉
> STATICFILES_DIRS = [os.path.join(BASE_DIR, "static"),]\
> #STATIC_ROOT = os.path.join(BASE_DIR, 'static')

5.上傳檔案

> python manage.py collectstatic

上傳成功後會出現<br />

> 130 static files copied to '...< Your static path>'.

6.同步static資料夾，將本地static資料夾中的新增檔案同步上傳至s3

> aws s3 sync static s3://<Your bucket name> --delete

Finish 2020/08/02



