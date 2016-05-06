#!/usr/bin/env python3

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


usage = """
{} svc_port server_name server_ip
""".format(sys.argv[0])

if len(sys.argv) != 4:
    print(usage)
    sys.exit(1)

data = {
    'username': 'user92',
    'password': '123'
}

from base_svc.comm import BaseAPIRequestHandler

rh = BaseAPIRequestHandler()
rh.set_argument('name', sys.argv[3])
rh.set_argument('ip', sys.argv[4])
kwargs = {}
kwargs['request_handler'] = rh

import base_api.balancer.balance_server
res = base_api.balancer.balance_server.save_server(sys.argv[3], sys.argv[4], **kwargs)
# if 'http_status' not in res or res['http_status'] != 200:
print(res)


