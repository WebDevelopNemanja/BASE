"""
Currency manipulation
"""

import MySQLdb

import base_common.msg
import base_lookup.currencies as cu
import base_lookup.api_messages as msgs
from base_common.dbacommon import app_api_method
from base_common.dbacommon import authenticated_call
from base_common.dbacommon import get_db
from base_common.dbacommon import params
from base_common.dbatransactions import update_currency_repo
from base_config.service import log

name = "currencies"
location = "currency"
request_timeout = 10


@authenticated_call()
@app_api_method(
    method='PUT',
    api_return=[
        (204, ''),
        (400, '')])
@params(
    {'arg': 'currency', 'type': str, 'required': True},
    {'arg': 'value', 'type': float, 'required': True},
)
def currency_add(currency, value, **kwargs):
    """
    Save currency
    """

    _db = get_db()
    dbc = _db.cursor()

    if currency not in cu.lmap:
        log.warning('Wrong or unregistered currency: {}'.format(currency))
        return base_common.msg.error(msgs.WRONG_CURRENCY)

    q = '''INSERT INTO currency (currency, value) VALUES ('{}', {})'''.format(currency, value)

    try:
        dbc.execute(q)
    except MySQLdb.IntegrityError as e:
        log.critical('Error save currency {} with value {}: {}'.format(currency, value, e))
        return base_common.msg.error(msgs.ERROR_ADDING_CURRENCY)

    _db.commit()
    _cur_id = dbc.lastrowid

    update_currency_repo(_cur_id, currency, value)

    return base_common.msg.put_ok()


@authenticated_call()
@app_api_method(
    method='GET',
    api_return=[
        (200, 'currency with value'),
        (400, '')])
@params(
    {'arg': 'currency', 'type': str, 'required': True},
)
def currency_get(currency, **kwargs):
    """
    Get currency
    """

    _db = get_db()
    dbc = _db.cursor()

    if currency not in cu.lmap:
        log.warning('Wrong or unregistered currency: {}'.format(currency))
        return base_common.msg.error(msgs.WRONG_CURRENCY)

    q = '''SELECT value from currency WHERE currency = '{}' order by id desc limit 1'''.format(currency)

    try:
        dbc.execute(q)
    except MySQLdb.IntegrityError as e:
        log.critical('Error getting currency {} from db: {}'.format(currency, e))
        return base_common.msg.error(msgs.ERROR_GET_CURRENCY)

    if dbc.rowcount != 1:
        log.warning("Found {} currencies {} in db".format(dbc.rowcount, currency))
        return base_common.msg.error(msgs.ERROR_GET_CURRENCY)

    _dbr = dbc.fetchone()
    _dbc = float(_dbr['value'])
    res = {}
    res[currency] = _dbc

    return base_common.msg.get_ok(res)
