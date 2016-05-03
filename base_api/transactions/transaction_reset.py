"""
Reset transactions
:description:
Reset user's transactions
and daily and account summaries.
Reset time recorded in user's data
"""

import datetime
import MySQLdb

from base_common.dbacommon import authenticated_call
from base_common.dbacommon import app_api_method
from base_common.dbacommon import params
from base_common.dbacommon import get_db
import base_lookup.api_messages as msgs
from base_config.service import log

name = "transaction_reset"
location = "transaction/reset"
request_timeout = 10


def _reset_summary(db, id_user, _datetime, id_reset_user, table):

    q = '''UPDATE
            {}
          SET
            reset_time = '{}',
            id_reset_user = '{}'
          WHERE
            id_user = '{}' and reset_time is null '''.format(table, _datetime, id_reset_user, id_user)

    dbc = db.cursor()
    try:
        dbc.execute(q)
    except MySQLdb.IntegrityError as e:
        log.critical('Error updating acount_summary for {}: {}'.format(id_user, e))
        return False

    return True


def _reset_account_summary(db, id_user, _datetime, id_reset_user):

    return _reset_summary(db, id_user, _datetime, id_reset_user, 'account_summary')


def _reset_daily_summary(db, id_user, _datetime, id_reset_user):

    return _reset_summary(db, id_user, _datetime, id_reset_user, 'daily_summary')


@authenticated_call()
@app_api_method(
    method='PATCH',
    api_return=[
        (204, ''),
        (400, msgs.msgs[msgs.WRONG_TRANSACTION_VALUE]),
        (400, msgs.msgs[msgs.ERROR_ADD_TRANSACTION])])
@params(
    {'arg': 'id_user', 'type': str, 'required': True},
)
def reset_transaction(id_user, **kwargs):
    """
    Reset transaction
    """

    _db = get_db()

    import base_common.dbatokens
    dbuser = base_common.dbatokens.get_user_by_token(_db, kwargs['auth_token'])

    _n = datetime.datetime.now()
    if not _reset_account_summary(_db, id_user, _n, dbuser.id_user):
        log.critical('Error reset account_summary')
        _db.rollback()
        return base_common.msg.error(msgs.ERROR_RESET_BALANCE)

    if not _reset_daily_summary(_db, id_user, _n, dbuser.id_user):
        log.critical('Error reset daily_summary')
        _db.rollback()
        return base_common.msg.error(msgs.ERROR_RESET_BALANCE)

    _db.commit()

    return base_common.msg.patch_ok()


