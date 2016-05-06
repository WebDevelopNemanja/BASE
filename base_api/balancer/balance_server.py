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


def _get_save_server_query(s_name, s_ip):

    n = datetime.datetime.now()
    return '''INSERT INTO
                balanced_servers
                (id, name, ip, created, active)
              VALUES
                (null, '{}', '{}', '{}', true)'''.format(s_name, s_ip, str(n))


@app_api_method(
    method='PUT',
    api_return=[(200, 'OK'), (404, 'notice')]
)
@params(
    {'arg': 'name', 'type': str, 'required': True, 'description': 'unique server name'},
    {'arg': 'ip', 'type': str, 'required': True, 'description': 'servers unique ip address'},
)
def save_server(name_server, ip_server, **kwargs):
    """
    Save balanced server
    """

    _db = get_db()
    dbc = _db.cursor()

    q = _get_save_server_query(name_server, ip_server)

    try:
        dbc.execute(q)
    except MySQLdb.IntegrityError as e:
        log.critical('Error saving server {} with address {}, error: {}'.format(name_server, ip_server, e))
        return base_common.msg.error(msgs.ERROR_ADD_SERVER)

    return base_common.msg.put_ok()


def _get_server_query(name_server, ip_server):

    q = '''SELECT id, name, ip, created, deactivated, active FROM balanced_servers  where {} = '{}' '''

    if name_server:
        return q.format('name', name_server)
    if ip_server:
        return q.format('ip', ip_server)

    return '''SELECT id, name, ip, created, deactivated, active FROM balanced_servers'''


@app_api_method(
    method='GET',
    api_return=[(200, 'OK'), (404, 'notice')]
)
@params(
    {'arg': 'name', 'type': str, 'required': False , 'description': 'unique server name'},
    {'arg': 'ip', 'type': str, 'required': False, 'description': 'servers unique ip address'},
)
def get_servers(name_server, ip_server, **kwargs):
    """
    Get balanced server
    """

    _db = get_db()
    dbc = _db.cursor()

    q = _get_server_query(name_server, ip_server)

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
            'created': qr['created'],
            'deactivated': qr['deactivated'],
            'active': qr['active']
        }

        res.append(srv)

    return base_common.msg.get_ok(res)


