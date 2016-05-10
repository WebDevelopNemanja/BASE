"""
Transaction manipulation
"""

import datetime
import json

import MySQLdb

import base_lookup.api_messages as msgs
import base_lookup.currencies as sc
import base_lookup.transaction_types as tt
from base_common.dbacommon import app_api_method
from base_common.dbacommon import authenticated_call
from base_common.dbacommon import get_db
from base_common.dbacommon import params
from base_common.seq import sequencer
from base_common.dbatransactions import get_currency_value
from base_config.service import log

name = "transaction"
location = "transaction"
request_timeout = 10


def _get_summary_id(db, id_user, db_query, db_tbl, seq_id):
    dbc = db.cursor()
    try:
        dbc.execute(db_query)
    except MySQLdb.IntegrityError as e:
        log.critical('Error getting {} for {}: {}'.format(db_tbl, id_user, e))
        return False, False

    if dbc.rowcount == 1:
        _db_r = dbc.fetchone()
        _r_id = _db_r['id']
        _r_c_id = _db_r['id_currency_change']
        return _r_id, True

    return sequencer().new(seq_id), False


def _get_account_summary_id(db, id_user, id_currency_change):
    q = '''SELECT
            id, id_currency_change
          FROM
            account_summary
          WHERE
            id_user = '{}' AND reset_time is null AND id_currency_change = {}'''.format(id_user, id_currency_change)

    return _get_summary_id(db, id_user, q, 'account_summary ', 'v')


def _get_daily_summary_id(db, id_user, id_currency_change):
    q = '''SELECT
            id, id_currency_change
          FROM
            daily_summary
          WHERE
              id_user = '{}'
            AND
              date = curdate()
            AND
              reset_time is null
            AND
              id_currency_change = {}'''.format(id_user, id_currency_change)

    return _get_summary_id(db, id_user, q, 'daily_summary', 'w')


def _get_transaction_query(transaction_id, id_user, datetime_now, transaction_type, transaction_value, referent_value,
                           id_currency_change, transaction_data):
    q = ''' INSERT INTO transactions
                  (id, id_user, transaction_time, transaction_type, value, referent_value, id_currency_change{})
            VALUES
                  ('{}', '{}', '{}', {}, {}, {}, {}{})'''.format(
        ', data' if transaction_data else '',
        transaction_id,
        id_user,
        datetime_now,
        transaction_type,
        transaction_value,
        referent_value,
        id_currency_change,
        ''', '{}' '''.format(transaction_data) if transaction_data else ''
    )

    return q


def _get_account_summary_query(as_id, id_user, update_summary, value, id_currency_change, tr_type):

    payin_value = value if tr_type in [tt.PAYIN, tt.WEB_PAYIN] else 0.00

    if update_summary:
        _q = '''UPDATE
                account_summary
              SET
                balance = balance + {}, payin_sum = payin_sum + {}
              WHERE
                id = '{}' '''.format(
                                value,
                                payin_value,
                                as_id)
    else:
        _q = '''INSERT INTO
                account_summary (id, id_user, balance, payin_sum, id_currency_change)
              VALUES
                ('{}', '{}', {}, {}, {})
                '''.format(as_id, id_user, value, payin_value, id_currency_change)

    return _q


def _get_daily_summary_query(summary_id, id_user, update_daily, value, id_currency_change, tr_type):

    if update_daily:
        _q = '''UPDATE
                    daily_summary
                SET
                  summary = summary + {}
                WHERE
                  id = '{}' '''.format(value, summary_id)
    else:
        _q = '''INSERT INTO daily_summary
                  (id, id_user, date, summary, id_currency_change)
                VALUES
                  ('{}', '{}', curdate(), {}, {})'''.format(
            summary_id, id_user, value, id_currency_change)

    return _q


def _check_value_by_transaction_type(transaction_type, value):

    if transaction_type in [tt.PAYIN, tt.WEB_PAYIN]:
        try:
            value = abs(value)
            return value
        except TypeError:
            return False

    if transaction_type in [tt.PAYOUT, tt.WEB_PAYOUT]:
        try:
            value = -abs(value)
            return value
        except TypeError:
            return False

    return value


@authenticated_call()
@app_api_method(
    method='PUT',
    uri='add',
    api_return=[
        (200, 'transaction ID'),
        (400, msgs.msgs[msgs.WRONG_TRANSACTION_VALUE]),
        (400, msgs.msgs[msgs.ERROR_ADD_TRANSACTION])])
@params(
    {'arg': 'transaction_type', 'type': int, 'required': True},
    {'arg': 'value', 'type': float, 'required': True},
    {'arg': 'currency', 'type': str, 'required': True},
    {'arg': 'data', 'type': json, 'required': False}
)
def transaction_add(transaction_type, value, currency, data, **kwargs):
    """
    Add transaction
    """

    _db = get_db()
    dbc = _db.cursor()

    import base_common.dbatokens
    dbuser = base_common.dbatokens.get_user_by_token(_db, kwargs['auth_token'])
    id_user = dbuser.id_user

    value = _check_value_by_transaction_type(transaction_type, value)
    if not value:
        log.warning('Invalid value {} from transaction type {}'.format(value, transaction_type))
        return base_common.msg.error(msgs.WRONG_TRANSACTION_VALUE)

    if currency not in sc.lmap:
        log.warning('Unknown currency: {}'.format(currency))
        return base_common.msg.error(msgs.WRONG_CURRENCY)

    referent_rate, id_currency_rate = get_currency_value(_db, currency)

    t_id = sequencer().new('t')
    a_id, update_account = _get_account_summary_id(_db, id_user, id_currency_rate)
    d_id, update_daily = _get_daily_summary_id(_db, id_user, id_currency_rate)

    _n = str(datetime.datetime.now())
    referent_value = value * referent_rate

    q = _get_transaction_query(t_id, id_user, _n, transaction_type, value, referent_value, id_currency_rate, data)
    try:
        dbc.execute(q)
    except MySQLdb.IntegrityError as e:
        log.critical('Error inserting transaction {} for user {}: {}'.format(t_id, id_user, e))
        _db.rollback()  # don't insert transaction after fail
        return base_common.msg.error(msgs.ERROR_ADD_TRANSACTION)

    qa = _get_account_summary_query(a_id, id_user, update_account, value, id_currency_rate, transaction_type)
    try:
        dbc.execute(qa)
    except MySQLdb.IntegrityError as e:
        log.critical('Error inserting/updating account_summary {} for {}: {}'.format(a_id, id_user, e))
        _db.rollback()  # don't insert transaction after fail
        return base_common.msg.error(msgs.ERROR_ADD_TRANSACTION)

    qd = _get_daily_summary_query(d_id, id_user, update_daily, value, id_currency_rate, transaction_type)
    try:
        dbc.execute(qd)
    except MySQLdb.IntegrityError as e:
        log.critical('Error inserting/updating daily_summary {} for {}: {}'.format(d_id, id_user, e))
        _db.rollback()  # don't insert transaction after fail
        return base_common.msg.error(msgs.ERROR_ADD_TRANSACTION)

    _db.commit()

    return base_common.msg.put_ok({'transaction_id': t_id})




