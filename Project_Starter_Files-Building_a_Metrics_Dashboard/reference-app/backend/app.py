from flask import Flask, render_template, request, jsonify
import logging
from jaeger_client import Config

import pymongo
from flask_pymongo import PyMongo

# def init_jaeger_tracer(service_name='backend'):
#     config= Config(config={}, service_name=service_name, validate=True)
#     return config.initialize_tracer()


def init_tracer(service):
    logging.getLogger('').handlers = []
    logging.basicConfig(format='%(message)s', level=logging.DEBUG)
    config = Config(
        config={
            'sampler': {
                'type': 'const',
                'param': 1,
            },
            'logging': True,
        },
        service_name=service,
    )
    # this call also sets opentracing.tracer
    return config.initialize_tracer()
tracer = init_tracer('backend')

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'example-mongodb'
app.config['MONGO_URI'] = 'mongodb://example-mongodb-svc.default.svc.cluster.local:27017/example-mongodb'

mongo = PyMongo(app)

@app.route('/')
def homepage():
    with tracer.start_span('Main backend route') as span:
        span.set_tag("Hello")
        return "Hello World"


@app.route('/api')
def my_api():
    with tracer.start_span("/api route") as span:
        answer = "something"
        span.set_tag("response;", answer)
        return jsonify(repsonse=answer)

@app.route('/star', methods=['POST'])
def add_star():
    with tracer.start_span("/star post") as span:
        star = mongo.db.stars
        name = request.json['name']
        distance = request.json['distance']
        star_id = star.insert({'name': name, 'distance': distance})
        new_star = star.find_one({'_id': star_id })
        output = {'name' : new_star['name'], 'distance' : new_star['distance']}
        span.set_tag(" posting output", output)
        return jsonify({'result' : output})

if __name__ == "__main__":
    app.run()
