# webfaction-asyncio-setup

Instructions for deploying an asyncio web app to WebFaction

Source: [Deploying a Tornado project in production using Github and WebFaction](http://skipperkongen.dk/2013/01/02/deploying-a-tornado-project-in-production-using-github-and-webfaction/)

# WebFaction panel steps

Go to the Websites page and click the `Create new application` button. Set the fields like this:

- App category: Custom
- App type: Custom websockets app (listening on port)
- URL: asyncio-test

After creating the Custom websockets app, make a note of the port.

# Install supervisor

```
pip2.7 install supervisor
```

You have to use Python 2.7 because supervisor does not yet run under Python 3.

# Install your code

```
git clone https://github.com/feihong/webfaction-asyncio-setup
cd asyncio-test
mkvirtualenv -p python3.5 asyncio-test
pip install -r requirements.txt
```
