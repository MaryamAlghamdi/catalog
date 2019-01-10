This is an item catalog Project for udacity Full Stack Web Developer Nano-degree Program its simple catalog for different courses information you will be able to make some modification after login using your face-book account.

______________________________________________________________#

Prerequisites:

1- you will have to install python3 , vm virtualbox with the appropriate vagrant version , gitbash terminal to work this project.
2- facebook account to login
______________________________________________________________#

Vagrant/VirtualBox, how to set it up:

Install VirtualBox:
VirtualBox is the software that actually runs the virtual machine. You can download it from (virtualbox.org) , here. Install the platform package for your operating system. You do not need the extension pack or the SDK. You do not need to launch VirtualBox after installing it; Vagrant will do that.

Install Vagrant:
Vagrant is the software that configures the VM and lets you share files between your host computer and the VM's filesystem. Download it from (vagrantup.com). Install the version for your operating system.
Windows users: The Installer may ask you to grant network permissions to Vagrant or make a firewall exception. Be sure to allow this.
If Vagrant is successfully installed, you will be able to run vagrant --version
in your terminal to see the version number.
The shell prompt in your terminal may differ. Here, the $ sign is the shell prompt



______________________________________________________________#

Running the project:

1- make sure that the Cdatabase.py, database_setup.py, project.py, templates and static folders , fb_client_secrets.json in the same directory in the vagrant folder
2- using the terminal change the directory to the catalog folder path
3- use (vagrant up) command terminal , next
4-use (vagrant ssh) command in the terminal
5- change directory to vagrant using (cd / vagrant) command
6-finally use (python or python3  project.py ) command to run the python code and git connect to the localhost:8000
7- list of the pages links of the project:
- Home Page :
- http://localhost:8000/
- Login Page:
- http://localhost:8000/login 
- Courses Page After Login Authorization : 
- http://localhost:8000/Lcourses/
- view Course With_Id_Num = 1 Items:  
- http://localhost:8000/Lcourses/Lcourses_id/lcList/ Ex: http://localhost:8000/Lcourses/1/lcList/
- Create New Course :
- http://localhost:8000/Lcourses/new/
- Edit Course With_Id_Num = 3 :
- http://localhost:8000/Lcourses/3/edit/
- Delete Course With_Id_Num = 3 :
- http://localhost:8000/Lcourses/3/delete/
- Create New Course Item To The Course With_Id_Num =3 :
- http://localhost:8000/Lcourses/3/lcList/new/
- Edit Item  with Id_Num = 20 and  Course With_Id_Num = 3 :
- http://localhost:8000/Lcourses/3/lcList/20/edit
- Delete Item with Id_Num = 20 and  Course With_Id_Num = 3 :
- http://localhost:8000/Lcourses/3/lcList/22/delete
- JSON LinkS  
- http://localhost:8000/Lcourses/JSON
- http://localhost:8000/Lcourses/3/lcList/JSON
- http://localhost:8000/Lcourses/3/lcList/19/JSON

______________________________________________________________#

Authors:
Mariam Alghamdi
Many instructions have been reached through :udacity.com - Full Stack Web Developer Nanodegree Program

