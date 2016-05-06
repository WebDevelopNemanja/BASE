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
    'name': sys.argv[2],
    'ip': sys.argv[3]
}

from base_svc.comm import call
import base_api.balancer.balance_server
res, status = call('localhost', sys.argv[1], base_api.balancer.balance_server.location, data, 'PUT')
print(res, status)
#
# try:
#     res = json.loads(res) if res else {}
# except Exception as e:
#     log_warning('Error load json data: {}'.format(res), '', None)
#     log_warning('Error: {}'.format(e), '', None)
#     result.update({'message': res})
#     res = {'message': res}
