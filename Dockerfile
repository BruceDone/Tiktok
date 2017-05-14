FROM python:3.5

MAINTAINER Bruce <nicefish66@gmail.com>

ENV WorkingDir /workspace/sanic

RUN mkdir -p ${WorkingDir}

COPY . ${WorkingDir}

WORKDIR ${WorkingDir}

RUN pip install -i 'http://mirrors.aliyun.com/pypi/simple/' -U -r ./requirements.txt --trusted-host mirrors.aliyun.com \
     && pip install git+https://github.com/BruceDone/py-dag.git
