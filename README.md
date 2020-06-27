# dropFile-deploy
## Intro & Demo
This program is for who don't want to spend time classifying documents by reading whole contents and manually replacing it. DropFile help you to automate this file-path replacement by NLP techniques.  
You can find demo in this link :   
We provide below feature :   
- web app (per local) that visualize each directory and file hierarchy
- file path recommendation and automation for building and reconstructing previously used directory  


## Project setup & Quick Start  
Only work in UNIX shell environment (For Windows users, recommend to use Ubuntu shell)  
Also need docker(here 19.03.8) and docker-compose(here 1.25.5)  
Docker : https://docs.docker.com/get-docker/  
Docker-Compose : https://docs.docker.com/compose/install/  
```
(after installing Docker and Docker-Compose)
/path/to/dropFile-deploy % source setting.sh
/path/to/dropFile-deploy % ROOT=(root_path) dropFile start (if you want to launch program and see web app)
/path/to/dropFile-deploy % dropFile open (if you want to see web app)  
/path/to/dropFile-deploy % dropFile stop (if you want to stop this whole program)
/path/to/dropFile-deploy % dropFile delete (if you want to uninstall whole environment setting)

```
If you start this process first time, it will takes some time since it is building web application environment from scratch.  
Also, if (root_path) is new directory hierarchy that has never initialized, it will also takes some time for initializing and preparing data.  
This program lazily update recommendation data to provide better recommendation. With not enough recommendation data accumulated, this program will mis-predict or never return file path for input upload file.  
We are currently linking OS download trigger into this web app. (2020.06.18)  
+) ROOT should not be "./data", this is metadata directory that store pickle value of DTM and word vocab


## Development Guide  
If you want to hack this code, just try below command and find out what's going on.  
```
/path/to/dropFile-deploy % source setting.sh
/path/to/dropFile-deploy % ROOT=(root_path) dropFile start (if you want to launch program and see web app)
/path/to/dropFile-deploy % dropFile bash (this will open docker container bash shell) 
/path/to/dropFile-deploy % dropFile logs (this will show actual log of what's going on)
```
