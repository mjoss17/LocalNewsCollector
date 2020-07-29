# Humanworthy  
  
## Installation  
Create a virtual enviroment  
```sudo pip3 install virtualenv```  
```virtualenv myprojectenv```  
Activate virtual enviroment  
```source myprojectenv/bin/activate```  
Clone the repo  
Install requirements in virtual enviroment  
```pip install -r LocalNewsCollector/webapp/requirements.txt```  
  
  
Create an empty db  
```python LocalNewsCollector/webapp/manage.py makemigrations```  
```python LocalNewsCollector/webapp/manage.py migrate```  

Collect Static
```python LocalNewsCollector/webapp/manage.py collectstatic```
  
Run the Server  
````python LocalNewsCollector/webapp/manage.py runserver 0.0.0.0:8000````  
  
## Workflow  
Make changes  
Run the server   
See how it look  
Push the good stuff  
Try it on prod  

## Server info  
Public DNS (IPv4):  
``ec2-100-26-239-139.compute-1.amazonaws.com``  
Ping Andrew for key  
  
  
### Workflow for updating server  
```ssh -i "LocalNews_KeyPair.pem" ubuntu@ec2-100-26-239-139.compute-1.amazonaws.com```  
```cd ~/django/LocalNewsCollector```  
```git pull```  
```sudo service apache2 restart```  
  
### In case of Emergency  
Follow this: https://medium.com/saarthi-ai/ec2apachedjango-838e3f6014ab  
and this: https://www.digitalocean.com/community/tutorials/how-to-serve-django-applications-with-apache-and-mod_wsgi-on-ubuntu-16-04  
and maybe even this: https://www.digitalocean.com/community/tutorials/how-to-install-the-apache-web-server-on-ubuntu-18-04  
