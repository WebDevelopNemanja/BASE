"""
User change password
:description:
changing password from forgot password flow
or from user change password request
"""

import tornado.web
import base_common.msg
from base_config.service import log
from base_lookup import api_messages as msgs
from base_common.app_hooks import format_password
from base_common.app_hooks import check_password
from base_common.dbacommon import get_db
from base_common.dbacommon import app_api_method
from base_common.dbatokens import authorized_by_token
from base_common.dbatokens import get_user_by_token
from base_common.dbacommon import get_url_token
from base_svc.comm import BaseAPIRequestHandler
import base_api.hash2params.retrieve_hash


name = "Change password"
location = "user/password/change.*"
request_timeout = 10


@app_api_method(
    method='POST',
    api_return=[(200, 'OK'), (404, '')]
)
def do_post(**kwargs):
    """
    Change password
    """

    _db = get_db()
    dbc = _db.cursor()
    request = kwargs['request_handler']

    try:
        newpassword = request.get_argument('newpassword')
    except tornado.web.MissingArgumentError:
        log.critical('Missing argument password')
        return base_common.msg.error(msgs.MISSING_REQUEST_ARGUMENT)

    # CHANGE PASSWORD FROM FORGOT PASSWORD FLOW
    h2p = get_url_token(request)
    if h2p and len(h2p) > 60:

        rh = BaseAPIRequestHandler()
        rh.set_argument('hash', h2p)
        rh.r_ip = request.r_ip
        kwargs['request_handler'] = rh
        res = base_api.hash2params.retrieve_hash.do_get(h2p, False, **kwargs)
        if 'http_status' not in res or res['http_status'] != 200:
            return base_common.msg.error(msgs.PASSWORD_TOKEN_EXPIRED)

        username = res['username']

    else:
        # TRY TO CHANGE PASSWORD FROM USER CHANGE REQUEST
        tk = request.auth_token
        if not authorized_by_token(_db, tk):
            return base_common.msg.error(msgs.UNAUTHORIZED_REQUEST)

        dbuser = get_user_by_token(_db, tk)
        if not dbuser.username:
            log.critical('User not found by token')
            return base_common.msg.error(msgs.UNAUTHORIZED_REQUEST)

        try:
            oldpassword = request.get_argument('oldpassword')
        except tornado.web.MissingArgumentError:
            log.critical('Missing argument oldpassword')
            return base_common.msg.error(msgs.MISSING_REQUEST_ARGUMENT)

        if not check_password(dbuser.password, dbuser.username, oldpassword):
            log.critical("Passwords don't match, entered : {}".format(oldpassword))
            return base_common.msg.error(msgs.WRONG_PASSWORD)

        username = dbuser.username

    # UPDATE USERS PASSWORD
    password = format_password(username, newpassword)

    uq = "update auth_users set password = '{}' where username = '{}'".format(
        password,
        username
    )

    try:
        dbc.execute(uq)
    except Exception as e:
        log.critical('Change password: {}'.format(e))
        return base_common.msg.error(msgs.USER_PASSWORD_CHANGE_ERROR)

    _db.commit()

    return base_common.msg.post_ok(msgs.USER_PASSWORD_CHANGED)

