"""
Balanced servers calls
:description:
manipulate server's data
"""

import datetime
import MySQLdb
import base_common.msg
from base_lookup import api_messages as msgs
from base_config.service import log
from base_common.dbacommon import params
from base_common.dbacommon import app_api_method
from base_common.dbacommon import get_db

name = "Balance Servers"
location = "balance/server"
request_timeout = 10


def _get_save_server_query(s_name, s_ip, port):

    n = datetime.datetime.now()
    return '''INSERT INTO
                balanced_servers
                (name, ip, port, created, active)
              VALUES
                ('{}', '{}', {}, '{}', true)'''.format(s_name, s_ip, port, str(n))


@app_api_method(
    method='PUT',
    api_return=[(200, 'OK'), (404, 'notice')]
)
@params(
    {'arg': 'name', 'type': str, 'required': True, 'description': 'unique server name'},
    {'arg': 'ip', 'type': str, 'required': True, 'description': 'servers ip address'},
    {'arg': 'port', 'type': int, 'required': True, 'description': 'services port'},
)
def save_server(name_server, ip_server, port, **kwargs):
    """
    Save balanced server
    """

    _db = get_db()
    dbc = _db.cursor()

    q = _get_save_server_query(name_server, ip_server, port)

    try:
        dbc.execute(q)
    except MySQLdb.IntegrityError as e:
        log.critical('Error saving server {} with address {}, error: {}'.format(name_server, ip_server, e))
        return base_common.msg.error(msgs.ERROR_ADD_SERVER)

    _db.commit()

    return base_common.msg.put_ok()


def _get_server_query(name_server, ip_server, port):

    q = '''SELECT id, name, ip, port, created, deactivated, active FROM balanced_servers  where {} '''

    if name_server:
        return q.format('''name = '{}' '''.format(name_server))
    if ip_server:
        return q.format('''ip = '{}' and port = {} '''.format(ip_server, port))

    return '''SELECT id, name, ip, created, deactivated, active FROM balanced_servers'''


@app_api_method(
    method='GET',
    api_return=[(200, 'OK'), (404, 'notice')]
)
@params(
    {'arg': 'name', 'type': str, 'required': False , 'description': 'unique server name'},
    {'arg': 'ip', 'type': str, 'required': False, 'description': 'servers unique ip address'},
    {'arg': 'port', 'type': int, 'required': False, 'description': 'service port'},
)
def get_servers(name_server, ip_server, port, **kwargs):
    """
    Get balanced server
    """

    _db = get_db()
    dbc = _db.cursor()

    q = _get_server_query(name_server, ip_server, port)

    try:
        dbc.execute(q)
    except MySQLdb.IntegrityError as e:
        log.critical('Error getting server {} with address {}, error: {}'.format(name_server, ip_server, e))
        return base_common.msg.error(msgs.ERROR_GET_SERVER)

    if dbc.rowcount != 1:
        log.critical('Found {} servers {} with address {}'.format(dbc.rowcount, name_server, ip_server))
        return base_common.msg.error(msgs.ERROR_GET_SERVER)

    res = []
    for qr in dbc.fetchall():

        srv = {
            'id_server': qr['id'],
            'name': qr['name'],
            'ip': qr['ip'],
            'port': qr['port'],
            'created': qr['created'],
            'deactivated': qr['deactivated'],
            'active': qr['active']
        }

        res.append(srv)

    return base_common.msg.get_ok(res)


