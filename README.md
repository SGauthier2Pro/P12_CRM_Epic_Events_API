# CRM_Epic_Events_API
***
##Introduction:

CRM_Epic_Events_API is an API which allows to manage customer relations for managing customers, contracts and event for  B2B firms.

This back-end system deliver a strong and secure interface for creating very special events for our cutomers

***
## Table of content
1. [General Info](#general-info)
2. [Technologies](#technologies)
3. [Installing Environment](#Installing-Environment)
4. [Configuring Environment](#Configuring-Environment)
5. [Starting Softdesk_API](#Starting-Softdesk_API)
6. [PEP8 reports](#PEP8-reports)
7. [FAQs](#faqs)
***
***
## General Info
***
This program is in version 1.0 and aimed the purpose why it has been created.
I wait the result of the meeting with the askers to see if there was some modifications to bring to this version.

***
## Technologies
***
List of technologies used within this project : 
* [Windows 10](https://www.microsoft.com/fr-fr/software-download/windows10): version 21H2
* [Python](https://www.python.org/downloads/release/python-3100/):  version 3.10.0
* [PyCharm](https://www.jetbrains.com/fr-fr/pycharm/): version 2021.2.3
* [git](https://git-scm.com/download/win): version 2.35.1.windows.2
* [Django](https://www.djangoproject.com/): version 4.1.7
* [django-filter](https://django-filter.readthedocs.io/en/stable/): version 22.1
* [djangorestframework](https://www.django-rest-framework.org): version 3.14.0
* [djangorestframework-simplejwt](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/): version 5.2.2
* [postgreqsl](https://www.postgresql.org/download/windows/): version 15.1
* [psycopg2](https://www.psycopg.org/docs/): version 2.9.6
* [pytest](https://docs.pytest.org/en/7.2.x/getting-started.html): version 7.2.2
* [drf-api-logger](https://pypi.org/project/drf-api-logger/): version 1.1.12 
* [pytest-django](https://pytest-django.readthedocs.io/en/latest/): version 4.5.2
* [pytest-reverse](https://pypi.org/project/pytest-reverse/): version 1.5.0
* [flake8](https://pypi.org/project/flake8/): Version 4.0.0
* [flake8-html](https://pypi.org/project/flake8-html/): version 0.4.2

***
## Installing Environment
***
This process suggests that you have admin privileges on you computer
### Python 3.10.0 installation
***
For installing Python 3.10.0 on your computer go to those address following the OS you use :

For MacOS :

  Package :
    [Python 3.10.0](https://www.python.org/ftp/python/3.10.0/python-3.10.0post2-macos11.pkg)
    
  Installation guide :
    [Installing Python 3 on MacOS](https://docs.python-guide.org/starting/install3/osx/)

For Linux :

  Package :
    [Python 3.10.0](https://www.python.org/downloads/release/python-3100/)
    [Gzipped source tarball](https://www.python.org/ftp/python/3.10.0/Python-3.10.0.tgz)
    [XZ compressed source tarball](https://www.python.org/ftp/python/3.10.0/Python-3.10.0.tar.xz)
    
 Installation guide :
    [Installing Python 3.10.0 on Linux](https://docs.python-guide.org/starting/install3/linux/)

For Windows :

  Package : 
    [Python 3.10.0](https://www.python.org/ftp/python/3.10.0/python-3.10.0-amd64.exe)
    
  Installation guide :
    [installing Python 3.1.0 on Windows](https://docs.python.org/fr/3/using/windows.html)

***
### Postrgresql installation
***
For installing Postrgresql on your computer go to this address :

Package :
[Postrgresql downloads](https://www.postgresql.org/download/)
you will find here installation package for you OS

Documentations: 
[postgresql documentation](https://www.postgresql.org/docs/)
you will find here all documentation you will need to install and configure your Postgresql server

After installing and configuring Postgresql, you have to create CRMEEDB database in your server :

The easiest and quickest way to do it is to use [PgAdmin4](https://www.pgadmin.org/download/)
Documentation is available [here](https://www.pgadmin.org/docs/pgadmin4/latest/index.html)

***
### Git 2.35.1 installation
***
For installing Git on your computer go to this adress (all OS contents):

[Git installation guide](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)

***
#### Git configuration 
***
(Even if you did not have done before, create an account on Github at the adress : https://github.com)

1. In order to configure your git IDs , see the following process in GitBash console :
   Type the following command
  
  ``` 
       $ git config --global user.name "your_github_username"
       $ git config --global user.email your_email@your_provider.com
  ```
2. Type the following command to configure the GitBash console interface (optional) :
  
  ```
       $ git config --global color.diff auto
       $ git config --global color.status auto 
       $ git config --global color.branch auto
  ```
***
### Clone the distant repository with Gitbash
***
You have now to clone the distant repository on your computer.
1. type the following command in Gitbash console :
  
  ```
        $ git clone https://github.com/SGauthier2Pro/P12_CRM_Epic_Events_API.git
  ```
***
## Configuring environment
***

***
### Restore database
***
use the following command from P12-CRM_Epic_Event_API folder to restore database :
```
psql -U username --set ON_ERROR_STOP=on -d CRMEEDB -f CRMEEDB_bkp
```

***
### Installation and execution with virtualenv
***
1. Move to P12_CRM_Epic_Events_API directory with ```$ cd P12_CRM_Epic_Events_API```
2. Create a virtual environment for the project with ```$ python -m venv env``` on windows or ```$ python3 -m venv env``` on macos or linux.
3. Activate the virtual environment with ```$ env\Scripts\activate.bat``` on windows or ```$ source env/bin/activate``` on macos or linux.
4. Install project dependencies with ```$ pip install -r requirements.txt```
5. Create an admin user for your server with ```$ python manage.py createsuperuser``` on windows or ```$ python3 manage.py createsuperuser``` on macos or linux.
6. Start the server with ```$ python manage.py runserver``` on windows or ```$ python3 manage.py runserver```on macos or linux.

***
## Starting CRM_Epic_Events_API
***
***
In order to use the API please refere you to the online documentation at this address:
https://documenter.getpostman.com/view/21154794/2s93m1ZPhJ

***
##Executing tests
***
   Run pytest with the following command from the app root directory:
      <code>P12_CRM_Epic_Events_API\crmepievents>pytest -v -s</code>

***
## PEP8 reports
***

In order to generate the flake8-html report, type the following command from the program folder :

```
    flake8 --format=html --htmldir=flake8-report --exclude env ../P12_CRM_Epic_Events_API
```  

***
***
## FAQs
***
***
N/A
***