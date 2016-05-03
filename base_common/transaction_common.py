import MySQLdb

import base_common.dbacommon
from base_config.service import log

__ACTIVE_CURRENCY = {}


def get_currency_value(db, currency):

    dbc = db.cursor()
    global __ACTIVE_CURRENCY

    if currency in __ACTIVE_CURRENCY:
        return __ACTIVE_CURRENCY[currency]['value'], __ACTIVE_CURRENCY[currency]['id']

    q = '''SELECT id, value from currency WHERE currency = '{}' order by id desc limit 1'''.format(currency)

    try:
        dbc.execute(q)
    except MySQLdb.IntegrityError as e:
        log.critical('Error getting currency {} from db: {}'.format(currency, e))
        return False

    if dbc.rowcount != 1:
        log.warning("Found {} currencies {} in db".format(dbc.rowcount, currency))
        return False

    _dbr = dbc.fetchone()
    _dbci = int(_dbr['id'])
    _dbcv = float(_dbr['value'])

    __ACTIVE_CURRENCY[currency] = {
        'id': _dbci,
        'value': _dbcv
    }

    return _dbcv, _dbci


def update_currency_repo(id_curr, currency, value):

    global __ACTIVE_CURRENCY
    __ACTIVE_CURRENCY[currency] = {
        'id': id_curr,
        'value': value
    }


def get_currency(currency_name):

    db = base_common.dbacommon.get_db()
    dbc = db.cursor()
    q = '''SELECT id, currency from currency where currency = '{}' '''.format(currency_name)

    try:
        dbc.execute(q)
    except MySQLdb.IntegrityError as e:
        log.critical('Error finding currency {} in db: {}'.format(currency_name, e))
        return False

    if dbc.rowcount != 1:
        log.critical('Found {} currencies {}'.format(dbc.rowcount, currency_name))
        return False

    qc = dbc.fetchone()
    return qc['currency']


