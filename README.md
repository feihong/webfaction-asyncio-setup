# webfaction-asyncio-setup

Instructions for deploying an asyncio web app to WebFaction

Sources:

- [Deploying a Tornado project in production using Github and WebFaction](http://skipperkongen.dk/2013/01/02/deploying-a-tornado-project-in-production-using-github-and-webfaction/)
- [Running django custom management commands with supervisord](http://serverfault.com/questions/390531/running-django-custom-management-commands-with-supervisord)

# WebFaction panel steps

Go to the Websites page and click the `Create new application` button. Set the fields like this:

- App category: Custom
- App type: Custom websockets app (listening on port)
- URL: asyncio-test

After creating the Custom websockets app, make a note of the port. Add newly-created application to one of your websites.

# Install your code

SSH into your server and run:

```
git clone https://github.com/feihong/webfaction-asyncio-setup
cd asyncio-test
mkvirtualenv -p python3.5 asyncio-test
pip install -r requirements.txt
```

Test that your app works by running

```
python app.py <port>
```

where `<port>` is the port you copied from the WebFaction panel. Open your browser and browse to the URL where you installed the app.

# Install supervisor

```
pip2.7 install supervisor
```

You have to use Python 2.7 because supervisor does not yet run under Python 3.

## Install supervisor config file

Inside `~/etc/supervisord.conf`, add something like this:

```
file=/tmp/supervisor.sock

[supervisord]
logfile=/home/you/tmp/supervisord.log
logfile_maxbytes=50MB
logfile_backups=10
loglevel=info
pidfile=/tmp/supervisord.pid

[rpcinterface:supervisor]
supervisor.rpcinterface_factory = supervisor.rpcinterface:make_main_rpcinterface

[supervisorctl]
serverurl=unix:////tmp/supervisor.sock

[program:asyncio_test]
command=bash /home/you/etc/asyncio-test.sh
directory=/home/you/webfaction-asyncio-setup/asyncio-test
```

## Install bash script to run your program

You will probably want to create a bash script that supervisor will use to run your program. Put the following code inside `~/etc/asyncio-test.sh`.
```

```bash
#!/bin/bash
source /home/you/.virtualenvs/asyncio-test/bin/activate
exec python app.py <port>
```

## Start supervisor

```
supervisord
```

## Stop supervisor

```
kill -QUIT <pid of supervisord>
```

## License

<a rel="license" href="http://creativecommons.org/licenses/by/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by/4.0/">Creative Commons Attribution 4.0 International License</a>.
