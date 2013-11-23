#!/usr/bin/env python2
import redis
import json
import gevent
import gevent.monkey
from gevent.pywsgi import WSGIServer
gevent.monkey.patch_all()

from flask import Flask, request, Response, render_template, jsonify

app = Flask(__name__)
redis_db = redis.StrictRedis(host='localhost', port=6379, db=1)
REDIS_PREFIX = 'kivy_flask_'
rgb = set(['r', 'g', 'b'])


def init_redis_db():
    for x in rgb:
        redis_db.set(REDIS_PREFIX + x, 0)


def rgba_stream():
    r = 0
    g = 0
    b = 0

    while True:
        new_rgb = (
            int(redis_db.get(REDIS_PREFIX + 'r')),
            int(redis_db.get(REDIS_PREFIX + 'g')),
            int(redis_db.get(REDIS_PREFIX + 'b')),
        )

        if new_rgb != (r, g, b):
            r, g, b = new_rgb

            yield 'data: %s\n\n' % json.dumps(
                {
                    'r': r,
                    'g': g,
                    'b': b,
                })

        gevent.sleep(0.001)


@app.route('/_send_rgb')
def set_rgb():
    r = request.args.get('red', False, type=int)
    g = request.args.get('green', False, type=int)
    b = request.args.get('blue', False, type=int)

    redis_db.set(REDIS_PREFIX + 'r', r)
    redis_db.set(REDIS_PREFIX + 'g', g)
    redis_db.set(REDIS_PREFIX + 'b', b)

    return jsonify(result='yeah')


@app.route('/rgb_source')
def rgba_request():
    return Response(
        rgba_stream(),
        mimetype='text/event-stream')


@app.route('/')
def page():
    return render_template('main.html')

if __name__ == '__main__':
    init_redis_db()
    http_server = WSGIServer(('127.0.0.1', 5002), app)
    http_server.serve_forever()
