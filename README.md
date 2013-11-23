# Flask Async

## Description

This is an example project with:

- [Flask](http://flask.pocoo.org/) asynchronous server
- [redis](http://redis.io/)
- Simple TCP non blocking server
- Simple [kivy](http://kivy.org) TCP client

## Usage

- First you need to install `redis`

- Create a virtualenv and install the requierements for the servers:

```sh
virtualenv venv
. ./venv/bin/activate
pip install -r async_server/requirements.txt
```

- Start both servers, on a différent terminal application (or in a tmux session):

```sh
python async_server/web_server/main.py  # for the Flask webserver
```

```sh
python async_server/tcp_server/server.py
```

- install the android application (.apk) locate in `kivy_app`, which is not signed and still in development state, or build your own with the source ;-)

Enjoy!
