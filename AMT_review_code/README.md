### Instruction for running the app on DigitalOcean ***Django droplet***

When logging into the server vis ssh, log into ```django``` not ```root``` user.
 
##### Install Anaconda Python 3.6 on the server 
 
##### 1. the labelling tool requires : 
```pip install --upgrade pip```  
	
```sudo pip --no-cache-dir install scipy```
  
  If there are some problems with some packages use the no cache argument when installing scipy.  
  
```sudo pip install scikit-image``` 
  
##### 2. from image label tool directory run: 
```sudo python setup.py install```

##### 3. edit the django_project settings.py, url.py, admin.py, etc.
In settings.py:

	STATIC_URL = '/static/'
	STATIC_ROOT = os.path.join(BASE_DIR, 'django_project/static')

	MEDIA_ROOT = os.path.join(BASE_DIR, 'django_project/media')
	MEDIA_URL = '/media/'

##### 4. add the example_labeller application in django_project directory: sudo python manage.py startapp example_labeller

##### 5. edit the ```/usr/local/lib/python2.7/dist-packages/Image_labelling_tool-0.1.dev1-py2.7.egg/image_labelling_tool/labelling_tool_views.py``` file as follows: 

	Comment ->  from django.views import View
	Add ->	from django.views.generic import TemplateView
	And change -> class LabellingToolView (TemplateView):  # View to TemplateView

***********************************************************************
### ONLY for slqlite: 
##### 6. Run:

```sudo python manage.py migrate```

##### 7. copy static folder to ```django_project/django_project```, also copy "jquery" folder from ext_static to static in django project

##### 8. Run:

```sudo python manage.py collectstatic``` 

##### 9. change the database from read only to read-write by -> ```sudo chown django:django db.sqlite3```

##### 10. Add some images:
1. make a folder in ```django/``` e.g. '```images```' and copy your images to it.
2. Run: ```sudo python manage.py populate ../images```	 

##### 11. sudo python manage.py createsuperuser ; and log in
******************************************************************************************


Ensuring SLL and HTTPS:
	Get a domain name and set it up (in DigitalOcean and Domain service (like Google)).
	And just watch this video: https://www.youtube.com/watch?v=z0L3u2Vn3Wo

```sudo apt-get update```

```sudo apt-get install git```

```cd /home/django/django_project/```

```git clone https://github.com/letsencrypt/letsencrypt```

```cd letsencrypt```

```sudo ./letsencrypt-auto --help```

```service nginx stop```

```sudo ./letsencrypt-auto certonly --standalone -d freeman.systems```  	#the last argument is the domain name

```sudo nano /etc/nginx/sites-available/django```

		And change -> server {
    			comment	->	#listen 80 default_server;
    			comment	->	#listen [::]:80 default_server ipv6only=on;
    			add	->	listen 443 ssl;

    			add	->	server_name freeman.systems;
    			add	->	ssl_certificate /etc/letsencrypt/live/freeman.systems/fullchain.pem;
    			add	->	ssl_certificate_key /etc/letsencrypt/live/freeman.systems/privkey.pem;
			
                        At the end add: (use 4 spaces for indentation)
					server {
    						listen 80;
    						server_name freeman.systems;
    						return 301 https://$host$request_uri;

					}
```service nginx restart```

***DONE! HTTPS Encryption ENABLED***
	

##### 12. In ```settings.py``` add security exception -> ```X_FRAME_OPTIONS = 'ALLOW-FROM https://workersandbox.mturk.com'``` to allow the page to be displayed in the MTurk frame.
This is for sandbox mode.
##### IMPORTATNT: In produciton mode add the correct AMT address: ```'ALLOW-FROM https://www.mturk.com'```

### 13. PostgreSQL setup:	

1. This should be already done by default, but somethings wrong: Disable Firewall on port 5432 -> ```sudo ufw allow 5432```

2. Allow the TCP/IP through port 5432 on the host IP:

```sudo find / -type f -name "pg_hba.conf"```

```nano pg_hba.conf```

add this line to pg_hba.conf, where x.x.x.x is the host IP ->: ```host all all x.x.x.x/24 trust```

```nano postgresql.conf```

add this line to postgresql.conf ->: ```listen_addresses = '*'```

 	




