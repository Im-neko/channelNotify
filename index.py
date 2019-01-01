#!/usr/bin/python
#-*- coding:utf-8 -*-
import json
import os
from os.path import join, dirname

from dotenv import load_dotenv
import falcon
import requests

# load .env file
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
SLACK_URL = os.environ.get("SLACK_URL")


class ChannelNotify():
    def on_get(self, req, res):
        res.status = falcon.HTTP_200
        res.body = json.dumps({'message': 'success'})

    def on_post(self, req, res):
        try:
            body = req.stream.read()
            data = json.loads(body)
            print(data)
            msg_type = data['event']['type'] # channel_created
            c_id = data['event']['channel']['id'] # channel id
            name = data['event']['channel']['name'] # created channel name
            text = msg_type+": <#"+c_id+"|"+name+">"
            requests.post(SLACK_URL, 
                          headers={"content-type":"application/json"}, 
                          data=json.dumps({'text':text}))
            res.status = falcon.HTTP_200
            res.body = json.dumps({'message': 'success'})
        except Exception as e:
            res.status = falcon.HTTP_500
            res.body = json.dumps({'message': str(e)})


api = falcon.API()
api.add_route('/', ChannelNotify())

if __name__ == '__main__':
    from wsgiref import simple_server
    httpd = simple_server.make_server("127.0.0.1", 17001, api)
    httpd.serve_forever()
    print("server is working on http://127.0.0.1:17001")
