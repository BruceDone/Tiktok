# Tiktok
<img src="imgs/tiktok.jpeg" >
Python web visualize build on the awesome web framework sanic ,it's inspired by the project of [dagobah](https://github.com/thieman/dagobah)


## Why use sanic 
While i using the dagobah ,which is based on the web framework of flask,and python version should be 2.x , after the app run a long time,the whole web page will broken and i have no choice except for restart it , after the deep research ,i do not have the reason why .so i just decide to use the sanic to replace the flask to see if it will fix this bug.


## How to use 
* environment
    * python:3.5.x
    * mongodb:3.2.x
    * docker-compose >= 1.11.2
* run with local
    * `pip install git+https://github.com/BruceDone/py-dag.git`
    * please start the mongo instance 
    * please edit the `src\config.yml ` MongoBackend section, update the host,port 
    * install the package `pip install -r requirements.txt`
    * `python run_app.py`
    * open the 'http://0.0.0.0:9000' in your browser 
* run with docker
    * please install the docker ,and docker-compose 
    * run `docker-compose build` in your shell 
    * run `docker-compose up -d` in your shell
    * open the 'http://0.0.0.0:9000' in your browser 

## Feature

* Manage multiple jobs scheduled with Cron syntax. Run times are shown in your local timezone.

<img src="http://i.imgur.com/PjPQedn.png" height="400">

* Tasks can be anything you'd normally run at a shell prompt. Pipe and redirect your heart out.

<img src="http://i.imgur.com/mWuQopx.png" height="400">

* Failed tasks don't break your entire job. Once you fix the task, the job picks up from where it left off.

<img src="http://i.imgur.com/u2vDre2.png" height="400">

* On completion and failure, Tiktok sends you an email summary of the executed job (just set it up in the config file).

<img src="http://i.imgur.com/yN6LUUZ.png" height="400">

* Tasks can even be [run on remote machines](https://github.com/thieman/dagobah/wiki/Adding-and-using-remote-hosts-in-Dagobah) (using your SSH config)
<img src="http://i.imgur.com/3sNjJiz.png" height="200">


## ToDo
- [ ] Login
- [ ] Send Email 
- [ ] Import and export job
- [ ] Remote task