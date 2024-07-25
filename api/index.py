from flask import Flask, jsonify, request
import os
import sys

app = Flask(__name__)

@app.route('/hello', methods=['GET'])
def hello():
    return jsonify(message="Hello from Flask on Vercel!")

@app.route('/purchase', methods=['POST'])
def purchase_ticket():
    # Your purchase logic here
    return jsonify(message="Purchase endpoint hit!")

def lambda_handler(event, context):
    from werkzeug.serving import make_server
    from werkzeug.wrappers import Response
    
    environ = {
        'wsgi.input': event['body'],
        'wsgi.errors': sys.stderr,
        'wsgi.version': (1, 0),
        'wsgi.url_scheme': event['headers']['x-forwarded-proto'],
        'wsgi.multithread': False,
        'wsgi.multiprocess': False,
        'wsgi.run_once': False,
        'SERVER_SOFTWARE': 'Werkzeug',
        'HTTP_HOST': event['headers']['host'],
        'REQUEST_METHOD': event['httpMethod'],
        'SCRIPT_NAME': '',
        'PATH_INFO': event['path'],
        'QUERY_STRING': event['queryStringParameters'],
        'CONTENT_TYPE': event.get('headers', {}).get('Content-Type', ''),
        'CONTENT_LENGTH': event.get('headers', {}).get('Content-Length', ''),
        'SERVER_NAME': 'localhost',
        'SERVER_PORT': '80',
    }

    response = make_server(environ).wsgi_app(environ, start_response)
    return {
        'statusCode': response.status_code,
        'headers': dict(response.headers),
        'body': response.data,
    }

def start_response(status, headers):
    return None
