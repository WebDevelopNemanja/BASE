import os
import sys
import json

pth = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(pth)

import base_common.dbatokens
import base_lookup.api_messages as amsgs
import base_lookup.transaction_types as tt
from base_tests.tests_common import WarningLevel, test
from base_tests.tests_common import log
from base_tests.tests_common import log_info
from base_tests.tests_common import make_base_url


def base_user_register_test(svc_port):
    log_info("User Register test", '', None)

    import base_api.users.user_register

    test(svc_port, base_api.users.user_register.location, 'GET', None,
         {'username': 'user1@test.loc', 'password': '123'}, 404, {'message': amsgs.msgs[amsgs.NOT_IMPLEMENTED_GET]})

    test(svc_port, base_api.users.user_register.location, 'POST', None,
         {'username': 'user1@test.loc', 'password': '123'}, 200, {'token': ''}, result_types={'token': str},
         warning_level=WarningLevel.STRICT_ON_KEY)

    test(svc_port, base_api.users.user_register.location, 'POST', None,
         {'username': 'user1@test.loc', 'password': '123'}, 400, {'message': amsgs.msgs[amsgs.USERNAME_ALREADY_TAKEN]})

    test(svc_port, base_api.users.user_register.location, 'POST', None,
         {'username': 'user2@test.loc', 'password': '123'}, 200, {'token': ''}, result_types={'token': str},
         warning_level=WarningLevel.STRICT_ON_KEY)

    test(svc_port, base_api.users.user_register.location, 'POST', None,
         {'username': 'user3@test.loc', 'password': '123'}, 200, {'token': ''}, result_types={'token': str},
         warning_level=WarningLevel.STRICT_ON_KEY)


def base_user_login_test(svc_port):
    log_info("User Login test", '', None)

    import base_api.users.user_login

    test(svc_port, base_api.users.user_login.location, 'POST', None, {'username': 'user1@test.loc', 'password': '123'},
         200, {'token': ''}, result_types={'token': str}, warning_level=WarningLevel.STRICT_ON_KEY)
    test(svc_port, base_api.users.user_login.location, 'POST', None,
         {'username': 'no_user@test.loc', 'password': '123'}, 400, {'message': amsgs.msgs[amsgs.USER_NOT_FOUND]})
    test(svc_port, base_api.users.user_login.location, 'POST', None, {'userna': 'no_user@test.loc', 'password': '123'},
         400, {'message': amsgs.msgs[amsgs.MISSING_REQUEST_ARGUMENT]})
    test(svc_port, base_api.users.user_login.location, 'POST', None, {'username': 'no_user@test.loc', 'passwo': '123'},
         400, {'message': amsgs.msgs[amsgs.MISSING_REQUEST_ARGUMENT]})


def base_user_logout_test(svc_port):
    log_info("User Logout test", '', None)

    import base_api.users.user_login
    import base_api.users.user_logout

    tk = test(svc_port, base_api.users.user_login.location, 'POST', None,
              {'username': 'user3@test.loc', 'password': '123'}, 200, {'token': ''}, result_types={'token': str},
              warning_level=WarningLevel.STRICT_ON_KEY)['token']

    test(svc_port, base_api.users.user_logout.location, 'POST', None, {}, 400,
         {'message': amsgs.msgs[amsgs.UNAUTHORIZED_REQUEST]})
    test(svc_port, base_api.users.user_logout.location, 'POST', tk, {}, 204, {})


def base_user_forgot_password_test(svc_port):
    log_info("User Forgot Password test", '', None)

    import base_api.users.forgot_password

    test(svc_port, base_api.users.forgot_password.location, 'POST', None, {'ername': 'user3@test.loc'}, 404,
         {'message': amsgs.msgs[amsgs.NOT_IMPLEMENTED_POST]})
    test(svc_port, base_api.users.forgot_password.location, 'PUT', None, {'ername': 'user3@test.loc'}, 400,
         {'message': amsgs.msgs[amsgs.MISSING_REQUEST_ARGUMENT]})
    test(svc_port, base_api.users.forgot_password.location, 'PUT', None, {'username': 'user4@test.loc'}, 400,
         {'message': amsgs.msgs[amsgs.USER_NOT_FOUND]})
    test(svc_port, base_api.users.forgot_password.location, 'PUT', None, {'username': 'user1@test.loc'}, 200, {})
    test(svc_port, base_api.users.forgot_password.location, 'PUT', None, {'username': 'user3@test.loc'}, 200, {})


def base_user_change_password_test(svc_port):
    log_info("User Change Password test", '', None)

    import base_api.users.user_login
    import base_api.hash2params.save_hash
    import base_api.users.change_password

    tk = test(svc_port, base_api.users.user_login.location, 'POST', None,
              {'username': 'user3@test.loc', 'password': '123'}, 200, {'token': ''}, result_types={'token': str},
              warning_level=WarningLevel.STRICT_ON_KEY)['token']
    htk = test(svc_port, base_api.hash2params.save_hash.location, 'PUT', None,
               {'data': json.dumps({"username": "user3@test.loc"})}, 200, {})['h']

    test(svc_port, base_api.users.change_password.location, 'POST', None, {'ername': 'user3@test.loc'}, 400,
         {'message': amsgs.msgs[amsgs.MISSING_REQUEST_ARGUMENT]})
    test(svc_port, base_api.users.change_password.location, 'POST', tk, {'newpassword': '123'}, 400,
         {'message': amsgs.msgs[amsgs.MISSING_REQUEST_ARGUMENT]})
    test(svc_port, base_api.users.change_password.location, 'POST', tk, {'newpassword': '123', 'oldpassword': '123'},
         200, {'message': amsgs.msgs[amsgs.USER_PASSWORD_CHANGED]}, result_types={'message': str})

    loc = base_api.users.change_password.location[:-2] + '/' + htk
    test(svc_port, loc, 'POST', None, {'newpassword': '123'}, 200, {'message': ''}, result_types={'message': str},
         warning_level=WarningLevel.STRICT_ON_KEY)


def base_user_check_test(svc_port):
    log_info("User Check test", '', None)

    import base_api.users.user_login
    import base_api.users.user_check

    tk = test(svc_port, base_api.users.user_login.location, 'POST', None,
              {'username': 'user3@test.loc', 'password': '123'}, 200, {'token': ''}, result_types={'token': str},
              warning_level=WarningLevel.STRICT_ON_KEY)['token']

    test(svc_port, base_api.users.user_check.location, 'POST', None, {'username': 'user2@test.loc', 'password': '123'},
         400, {'message': amsgs.msgs[amsgs.UNAUTHORIZED_REQUEST]})
    test(svc_port, base_api.users.user_check.location, 'POST', tk, {'username': 'user2@test.loc', 'password': '123'},
         200, {'username': ''}, result_types={'username': str}, warning_level=WarningLevel.STRICT_ON_KEY)


def base_hash_save_test(svc_port):
    log_info("Hash save test", '', None)

    import base_api.hash2params.save_hash

    test(svc_port, base_api.hash2params.save_hash.location, 'POST', None,
         {'username': 'user2@test.loc', 'password': '123'}, 404, {'message': amsgs.msgs[amsgs.NOT_IMPLEMENTED_POST]})
    test(svc_port, base_api.hash2params.save_hash.location, 'PUT', None, {'dat': 'user2@test.loc'}, 400,
         {'message': amsgs.msgs[amsgs.MISSING_REQUEST_ARGUMENT]})
    test(svc_port, base_api.hash2params.save_hash.location, 'PUT', None,
         {'data': json.dumps({"username": "user2@test.loc"})}, 200, {})


def base_hash_retrieve_test(svc_port):
    log_info("Hash Retrieve test", '', None)

    import base_api.hash2params.save_hash
    import base_api.hash2params.retrieve_hash

    htk = test(svc_port, base_api.hash2params.save_hash.location, 'PUT', None,
               {'data': json.dumps({"username": "user2@test.loc"})}, 200, {})['h']

    test(svc_port, base_api.hash2params.retrieve_hash.location, 'PUT', None, {'hash': htk}, 404,
         {'message': amsgs.msgs[amsgs.NOT_IMPLEMENTED_PUT]})
    test(svc_port, base_api.hash2params.retrieve_hash.location, 'GET', None,
         {'hash': htk[:20]}, 400, {'message': ''}, warning_level=WarningLevel.STRICT_ON_KEY)
    test(svc_port, base_api.hash2params.retrieve_hash.location, 'GET', None,
         {'hash': htk}, 200, {})


def base_user_change_username_test(svc_port):
    log_info("User Change Username test", '', None)

    import base_api.users.user_login
    import base_api.users.change_username

    tk = test(svc_port, base_api.users.user_login.location, 'POST', None,
              {'username': 'user1@test.loc', 'password': '123'}, 200, {'token': ''}, result_types={'token': str},
              warning_level=WarningLevel.STRICT_ON_KEY)['token']

    test(svc_port, base_api.users.change_username.location, 'POST', None, {'username': '', 'password': ''},
         400, {'message': amsgs.msgs[amsgs.UNAUTHORIZED_REQUEST]})
    test(svc_port, base_api.users.change_username.location, 'POST', tk, {'username': 'user21@test.loc'}, 400,
         {'message': amsgs.msgs[amsgs.MISSING_REQUEST_ARGUMENT]})
    test(svc_port, base_api.users.change_username.location, 'POST', tk,
         {'username': 'user21@test.loc', 'password': '12'}, 400, {'message': amsgs.msgs[amsgs.WRONG_PASSWORD]})
    test(svc_port, base_api.users.change_username.location, 'POST', tk,
         {'username': 'user21@test.loc', 'password': '123'}, 200,
         {'message': amsgs.msgs[amsgs.CHANGE_USERNAME_REQUEST]}, result_types={'message': str})


def base_user_changing_username_test(svc_port):
    log_info("Changing Username test", '', None)

    import base_api.users.user_login
    import base_api.hash2params.save_hash
    import base_api.users.change_username
    import base_api.users.changing_username

    tk = test(svc_port, base_api.users.user_login.location, 'POST', None,
              {'username': 'user1@test.loc', 'password': '123'}, 200, {'token': ''}, result_types={'token': str},
              warning_level=WarningLevel.STRICT_ON_KEY)['token']

    import base_common.dbacommon
    import base_tests.tests_common

    _db = base_common.dbacommon.get_db('test_')
    dbuser = base_common.dbatokens.get_user_by_token(_db, tk, log)

    test(svc_port, base_api.users.change_username.location, 'POST', tk,
         {'username': 'user21@test.loc', 'password': '123'}, 200,
         {'message': amsgs.msgs[amsgs.CHANGE_USERNAME_REQUEST]}, result_types={'message': str})

    htk = base_tests.tests_common.parse_hash_from_change_username_mail(_db, 'user21@test.loc')

    loc = base_api.users.changing_username.location[:-2] + htk
    test(svc_port, loc, 'GET', None, {}, 200, {'message': amsgs.msgs[amsgs.USER_NAME_CHANGED]},
         result_types={'message': str})
    test(svc_port, loc, 'GET', None, {}, 400, {'message': amsgs.msgs[amsgs.PASSWORD_TOKEN_EXPIRED]},
         result_types={'message': str})

    test(svc_port, base_api.users.change_username.location, 'POST', tk,
         {'username': 'user1@test.loc', 'password': '123'}, 200,
         {'message': amsgs.msgs[amsgs.CHANGE_USERNAME_REQUEST]}, result_types={'message': str})

    htk1 = base_tests.tests_common.parse_hash_from_change_username_mail(_db, 'user1@test.loc')

    loc1 = base_api.users.changing_username.location[:-2] + htk1
    test(svc_port, loc1, 'GET', None, {}, 200, {'message': amsgs.msgs[amsgs.USER_NAME_CHANGED]},
         result_types={'message': str})


def base_save_message_test(svc_port):
    log_info("Email Message Save test", '', None)

    # SEND MAIL IS NOT REGISTERED FOR API
    import base_api.mail_api.save_mail

    test(svc_port, base_api.mail_api.save_mail.location, 'POST', None,
         {'username': 'user21@test.loc', 'password': '123'}, 404, {'message': ''},
         warning_level=WarningLevel.STRICT_ON_KEY)


def base_set_option_test(svc_port):
    log_info("Save Option test", '', None)

    import base_api.users.user_login
    import base_api.options.options
    from base_api.options.options import set_option

    tk = test(svc_port, base_api.users.user_login.location, 'POST', None,
              {'username': 'user3@test.loc', 'password': '123'}, 200, {'token': ''}, result_types={'token': str},
              warning_level=WarningLevel.STRICT_ON_KEY)['token']

    test(svc_port, '{}/{}'.format(base_api.options.options.location, set_option.__api_path__), 'PUT', None,
         {'option_name': 'test_option', 'option_value': 'test_value'}, 400,
         {'message': amsgs.msgs[amsgs.UNAUTHORIZED_REQUEST]}, result_types={'message': str})
    test(svc_port, '{}/{}'.format(base_api.options.options.location, set_option.__api_path__), 'PUT', tk,
         {'option_name': 'test_option', 'option_value': 'test_value'}, 204, {})
    test(svc_port, '{}/{}'.format(base_api.options.options.location, set_option.__api_path__), 'PUT', tk,
         {'option_name': 'test_option', 'option_value': 'test_value'}, 204, {})
    test(svc_port, '{}/{}'.format(base_api.options.options.location, set_option.__api_path__), 'PUT', tk,
         {'option_name': 'test_option', 'option_value': True}, 204, {})
    test(svc_port, '{}/{}'.format(base_api.options.options.location, set_option.__api_path__), 'PUT', tk,
         {'option_name': 'test_option', 'option_value': 1}, 204, {})
    test(svc_port, '{}/{}'.format(base_api.options.options.location, set_option.__api_path__), 'PUT', tk,
         {'option_name': 'test_option', 'option_value': 1.090232}, 204, {})
    test(svc_port, '{}/{}'.format(base_api.options.options.location, set_option.__api_path__), 'PUT', tk,
         {'option_name': 'test_option', 'option_value': json.dumps({'key': 'val'})}, 204, {})


def base_get_option_test(svc_port):
    log_info("Get Option test", '', None)

    import base_api.users.user_login
    import base_api.options.options
    from base_api.options.options import set_option, get_option

    tk = test(svc_port, base_api.users.user_login.location, 'POST', None,
              {'username': 'user3@test.loc', 'password': '123'}, 200, {'token': ''}, result_types={'token': str},
              warning_level=WarningLevel.STRICT_ON_KEY)['token']

    test(svc_port, '{}/{}'.format(base_api.options.options.location, set_option.__api_path__), 'PUT', None,
         {'option_name': 'test_option', 'option_value': 'test_value'}, 400,
         {'message': amsgs.msgs[amsgs.UNAUTHORIZED_REQUEST]}, result_types={'message': str})
    test(svc_port, '{}/{}'.format(base_api.options.options.location, set_option.__api_path__), 'PUT', tk,
         {'option_name': 'test_option', 'option_value': 'test_value'}, 204, {})
    test(svc_port, '{}/{}'.format(base_api.options.options.location, set_option.__api_path__), 'PUT', tk,
         {'option_name': 'test1_option', 'option_value': 'test_value'}, 204, {})
    test(svc_port, '{}/{}'.format(base_api.options.options.location, set_option.__api_path__), 'PUT', tk,
         {'option_name': 'test2_option', 'option_value': True}, 204, {})
    test(svc_port, '{}/{}'.format(base_api.options.options.location, set_option.__api_path__), 'PUT', tk,
         {'option_name': 'test3_option', 'option_value': 1}, 204, {})
    test(svc_port, '{}/{}'.format(base_api.options.options.location, set_option.__api_path__), 'PUT', tk,
         {'option_name': 'test4_option', 'option_value': 1.090232}, 204, {})
    test(svc_port, '{}/{}'.format(base_api.options.options.location, set_option.__api_path__), 'PUT', tk,
         {'option_name': 'test5_option', 'option_value': json.dumps({'key': 'val'})}, 204, {})
    test(svc_port, '{}/{}'.format(base_api.options.options.location, set_option.__api_path__), 'PUT', tk,
         {'option_name': 'test_datetime', 'option_value': '2016-02-22 12:05:11'}, 204, {})

    test(svc_port, '{}/{}'.format(base_api.options.options.location, get_option.__api_path__), 'GET', None,
         {'option_name': 'test_option'}, 400, {'message': amsgs.msgs[amsgs.UNAUTHORIZED_REQUEST]},
         result_types={'message': str})
    test(svc_port, '{}/{}'.format(base_api.options.options.location, get_option.__api_path__), 'GET', tk,
         {'option_name': 'test_option'}, 200, {'test_option': 'test_value'}, result_types={'test_option': str})
    test(svc_port, '{}/{}'.format(base_api.options.options.location, get_option.__api_path__), 'GET', tk,
         {'option_name': 'test1_option'}, 200, {'test1_option': 'test_value'}, result_types={'test1_option': str})
    test(svc_port, '{}/{}'.format(base_api.options.options.location, get_option.__api_path__), 'GET', tk,
         {'option_name': 'test2_option'}, 200, {'test2_option': 'True'}, result_types={'test2_option': str})
    test(svc_port, '{}/{}'.format(base_api.options.options.location, get_option.__api_path__), 'GET', tk,
         {'option_name': 'test3_option'}, 200, {'test3_option': '1'}, result_types={'test3_option': str})
    test(svc_port, '{}/{}'.format(base_api.options.options.location, get_option.__api_path__), 'GET', tk,
         {'option_name': 'test4_option'}, 200, {'test4_option': '1.090232'}, result_types={'test4_option': str})
    test(svc_port, '{}/{}'.format(base_api.options.options.location, get_option.__api_path__), 'GET', tk,
         {'option_name': 'test5_option'}, 200, {'test5_option': '{"key": "val"}'}, result_types={'test5_option': str})
    test(svc_port, '{}/{}'.format(base_api.options.options.location, get_option.__api_path__), 'GET', tk,
         {'option_name': 'test_datetime'}, 200, {'test_datetime': '2016-02-22 12:05:11'},
         result_types={'test_datetime': str})


def base_del_option_test(svc_port):
    log_info("Delete Option test", '', None)

    import base_api.users.user_login
    import base_api.options.options
    from base_api.options.options import del_option

    tk = test(svc_port, base_api.users.user_login.location, 'POST', None,
              {'username': 'user3@test.loc', 'password': '123'}, 200, {'token': ''}, result_types={'token': str},
              warning_level=WarningLevel.STRICT_ON_KEY)['token']

    test(svc_port, '{}/{}'.format(base_api.options.options.location, del_option.__api_path__), 'DELETE', None,
         {'option_name': 'test_option'}, 400, {'message': amsgs.msgs[amsgs.UNAUTHORIZED_REQUEST]},
         result_types={'message': str})
    test(svc_port, '{}/{}'.format(base_api.options.options.location, del_option.__api_path__), 'DELETE', tk,
         {'option_name': 'test_option'}, 204, {})
    test(svc_port, '{}/{}'.format(base_api.options.options.location, del_option.__api_path__), 'DELETE', tk,
         {'option_name': 'test1_option'}, 204, {})
    test(svc_port, '{}/{}'.format(base_api.options.options.location, del_option.__api_path__), 'DELETE', tk,
         {'option_name': 'test2_option'}, 204, {})
    test(svc_port, '{}/{}'.format(base_api.options.options.location, del_option.__api_path__), 'DELETE', tk,
         {'option_name': 'test3_option'}, 204, {})
    test(svc_port, '{}/{}'.format(base_api.options.options.location, del_option.__api_path__), 'DELETE', tk,
         {'option_name': 'test4_option'}, 204, {})
    test(svc_port, '{}/{}'.format(base_api.options.options.location, del_option.__api_path__), 'DELETE', tk,
         {'option_name': 'test5_option'}, 204, {})


def show_api_spec_test(svc_port):
    log_info("Show API Specification test", '', None)

    test(svc_port, 'spec', 'GET', None, {}, 200, {'api_version': '', 'status': '', 'applications': ''},
         result_types={'api_version': str, 'status': int, 'applications': dict},
         warning_level=WarningLevel.STRICT_ON_KEY)
    test(svc_port, 'spec', 'DELETE', None, {}, 405, {})
    test(svc_port, 'spec?html=true', 'GET', None, {}, 200, {'message': '', 'status': 200},
         result_types={'message': str, 'status': int}, warning_level=WarningLevel.STRICT_ON_KEY)


def save_currency_test(svc_port):
    log_info("Save Currency test", '', None)

    import base_api.users.user_login
    import base_api.transactions.currency

    tku = test(svc_port, make_base_url(base_api.users.user_login.location), 'POST', None,
               {'username': 'user1@test.loc', 'password': '123'}, 200, {'token': ''}, result_types={'token': str},
               warning_level=WarningLevel.STRICT_ON_KEY)['token']

    test(svc_port, make_base_url(base_api.transactions.currency.location), 'POST', None, {}, 404,
         {'message': amsgs.msgs[amsgs.NOT_IMPLEMENTED_POST]})
    test(svc_port, make_base_url(base_api.transactions.currency.location), 'PUT', None, {}, 400,
         {'message': amsgs.msgs[amsgs.UNAUTHORIZED_REQUEST]})
    test(svc_port, make_base_url(base_api.transactions.currency.location), 'PUT', tku, {}, 400,
         {'message': amsgs.msgs[amsgs.MISSING_REQUEST_ARGUMENT]})

    test(svc_port, make_base_url(base_api.transactions.currency.location), 'PUT', tku,
         {'currency': 'RSD', 'value': 120.00}, 204, {})
    test(svc_port, make_base_url(base_api.transactions.currency.location), 'PUT', tku,
         {'currency': 'RSD', 'value': 122.20}, 204, {})
    test(svc_port, make_base_url(base_api.transactions.currency.location), 'PUT', tku,
         {'currency': 'RSD', 'value': 121.50}, 204, {})

    test(svc_port, make_base_url(base_api.transactions.currency.location), 'PUT', tku,
         {'currency': 'EUR', 'value': 1.00}, 204, {})


def get_currency_test(svc_port):
    log_info("Get Currency test", '', None)

    import base_api.users.user_login
    import base_api.transactions.currency

    tku = test(svc_port, base_api.users.user_login.location, 'POST', None,
               {'username': 'user1@test.loc', 'password': '123'}, 200, {'token': ''}, result_types={'token': str},
               warning_level=WarningLevel.STRICT_ON_KEY)['token']

    test(svc_port, make_base_url(base_api.transactions.currency.location), 'POST', None, {}, 404,
         {'message': amsgs.msgs[amsgs.NOT_IMPLEMENTED_POST]})
    test(svc_port, make_base_url(base_api.transactions.currency.location), 'GET', None, {}, 400,
         {'message': amsgs.msgs[amsgs.UNAUTHORIZED_REQUEST]})
    test(svc_port, make_base_url(base_api.transactions.currency.location), 'GET', tku, {}, 400,
         {'message': amsgs.msgs[amsgs.MISSING_REQUEST_ARGUMENT]})

    test(svc_port, make_base_url(base_api.transactions.currency.location), 'GET', tku, {'currency': 'RSD'}, 200, {})
    test(svc_port, make_base_url(base_api.transactions.currency.location), 'GET', tku, {'currency': 'RSD'}, 200,
         {'RSD': 121.50}, result_types={'RSD': float})

    test(svc_port, make_base_url(base_api.transactions.currency.location), 'GET', tku, {'currency': 'EUR'}, 200, {})
    test(svc_port, make_base_url(base_api.transactions.currency.location), 'GET', tku, {'currency': 'EUR'}, 200,
         {'EUR': 1.00}, result_types={'EUR': float})


def add_transaction_test(svc_port):
    log_info("Add Transaction test", '', None)

    import base_api.transactions.transaction
    import base_api.users.user_login

    tk = test(svc_port, base_api.users.user_login.location, 'POST', None,
              {'username': 'user2@test.loc', 'password': '123'}, 200, {'token': ''}, result_types={'token': str},
              warning_level=WarningLevel.STRICT_ON_KEY)['token']

    test(svc_port, make_base_url(base_api.transactions.transaction.location,
                                 base_api.transactions.transaction.transaction_add.__api_path__),
         'POST', None, {}, 404, {'message': amsgs.msgs[amsgs.NOT_IMPLEMENTED_POST]})
    test(svc_port, make_base_url(base_api.transactions.transaction.location,
                                 base_api.transactions.transaction.transaction_add.__api_path__),
         'PUT', None, {}, 400, {'message': amsgs.msgs[amsgs.UNAUTHORIZED_REQUEST]})
    test(svc_port, make_base_url(base_api.transactions.transaction.location,
                                 base_api.transactions.transaction.transaction_add.__api_path__), 'PUT', tk, {}, 400,
         {'message': amsgs.msgs[amsgs.MISSING_REQUEST_ARGUMENT]})

    test(svc_port, make_base_url(base_api.transactions.transaction.location,
                                 base_api.transactions.transaction.transaction_add.__api_path__), 'PUT', tk,
         {'transaction_type': tt.PAYIN, 'value': 5.011, 'currency': 'RSD'}, 200,
         {'transaction_id': ''}, result_types={'transaction_id': str}, warning_level=WarningLevel.STRICT_ON_KEY)
    test(svc_port, make_base_url(base_api.transactions.transaction.location,
                                 base_api.transactions.transaction.transaction_add.__api_path__), 'PUT', tk,
         {'transaction_type': tt.WEB_PAYIN, 'value': 4.011, 'currency': 'RSD'}, 200,
         {'transaction_id': ''}, result_types={'transaction_id': str}, warning_level=WarningLevel.STRICT_ON_KEY)
    test(svc_port, make_base_url(base_api.transactions.transaction.location,
                                 base_api.transactions.transaction.transaction_add.__api_path__), 'PUT', tk,
         {'transaction_type': tt.PAYOUT, 'value': 2.011, 'currency': 'RSD'}, 200,
         {'transaction_id': ''}, result_types={'transaction_id': str}, warning_level=WarningLevel.STRICT_ON_KEY)
    test(svc_port, make_base_url(base_api.transactions.transaction.location,
                                 base_api.transactions.transaction.transaction_add.__api_path__), 'PUT', tk,
         {'transaction_type': tt.WEB_PAYOUT, 'value': 3.011, 'currency': 'RSD'}, 200,
         {'transaction_id': ''}, result_types={'transaction_id': str}, warning_level=WarningLevel.STRICT_ON_KEY)

    test(svc_port, make_base_url(base_api.transactions.transaction.location,
                                 base_api.transactions.transaction.transaction_add.__api_path__), 'PUT', tk,
         {'transaction_type': tt.PAYIN, 'value': -1.011, 'currency': 'RSD'}, 200,
         {'transaction_id': ''}, result_types={'transaction_id': str}, warning_level=WarningLevel.STRICT_ON_KEY)
    test(svc_port, make_base_url(base_api.transactions.transaction.location,
                                 base_api.transactions.transaction.transaction_add.__api_path__), 'PUT', tk,
         {'transaction_type': tt.WEB_PAYIN, 'value': -1.011, 'currency': 'RSD'}, 200,
         {'transaction_id': ''}, result_types={'transaction_id': str}, warning_level=WarningLevel.STRICT_ON_KEY)
    test(svc_port, make_base_url(base_api.transactions.transaction.location,
                                 base_api.transactions.transaction.transaction_add.__api_path__), 'PUT', tk,
         {'transaction_type': tt.PAYOUT, 'value': -1.011, 'currency': 'RSD'}, 200,
         {'transaction_id': ''}, result_types={'transaction_id': str}, warning_level=WarningLevel.STRICT_ON_KEY)
    test(svc_port, make_base_url(base_api.transactions.transaction.location,
                                 base_api.transactions.transaction.transaction_add.__api_path__), 'PUT', tk,
         {'transaction_type': tt.WEB_PAYOUT, 'value': -1.011, 'currency': 'RSD'}, 200,
         {'transaction_id': ''}, result_types={'transaction_id': str}, warning_level=WarningLevel.STRICT_ON_KEY)

    test(svc_port, make_base_url(base_api.transactions.transaction.location,
                                 base_api.transactions.transaction.transaction_add.__api_path__), 'PUT', tk,
         {'transaction_type': tt.PAYIN, 'value': 6.0, 'currency': 'RSD',
          'data': json.dumps({'ref': 'xxxx'})}, 200, {'transaction_id': ''}, result_types={'transaction_id': str},
         warning_level=WarningLevel.STRICT_ON_KEY)

    # tka = test(svc_port, base_api.users.user_login.location, 'POST', None,
    #            {'username': 'admin1@test.loc', 'password': '123'}, 200, {'token': ''}, result_types={'token': str},
    #            warning_level=WarningLevel.STRICT_ON_KEY)['token']

    import base_api.transactions.currency
    test(svc_port, make_base_url(base_api.transactions.currency.location), 'PUT', tk,
         {'currency': 'RSD', 'value': 123.50}, 204, {})
    test(svc_port, make_base_url(base_api.transactions.transaction.location,
                                 base_api.transactions.transaction.transaction_add.__api_path__), 'PUT', tk,
         {'transaction_type': tt.PAYIN, 'value': 5.011, 'currency': 'RSD'}, 200,
         {'transaction_id': ''}, result_types={'transaction_id': str}, warning_level=WarningLevel.STRICT_ON_KEY)
    test(svc_port, make_base_url(base_api.transactions.currency.location), 'PUT', tk,
         {'currency': 'RSD', 'value': 122.70}, 204, {})
    test(svc_port, make_base_url(base_api.transactions.transaction.location,
                                 base_api.transactions.transaction.transaction_add.__api_path__), 'PUT', tk,
         {'transaction_type': tt.PAYIN, 'value': 5.011, 'currency': 'RSD'}, 200,
         {'transaction_id': ''}, result_types={'transaction_id': str}, warning_level=WarningLevel.STRICT_ON_KEY)


def reset_transaction_test(svc_port):
    log_info("Reset Transaction test", '', None)

    import base_api.users.user_login
    import base_api.transactions.transaction_reset

    tku = test(svc_port, base_api.users.user_login.location, 'POST', None,
               {'username': 'user2@test.loc', 'password': '123'}, 200, {'token': ''}, result_types={'token': str},
               warning_level=WarningLevel.STRICT_ON_KEY)['token']
    tku1 = test(svc_port, base_api.users.user_login.location, 'POST', None,
                {'username': 'user3@test.loc', 'password': '123'}, 200, {'token': ''}, result_types={'token': str},
                warning_level=WarningLevel.STRICT_ON_KEY)['token']

    _db = base_common.dbacommon.get_db('test_')
    dbuser1 = base_common.dbatokens.get_user_by_token(_db, tku1, is_active=False)

    test(svc_port, make_base_url(base_api.transactions.transaction_reset.location), 'POST', None, {}, 404,
         {'message': amsgs.msgs[amsgs.NOT_IMPLEMENTED_POST]})
    test(svc_port, make_base_url(base_api.transactions.transaction_reset.location), 'PATCH', None, {}, 400,
         {'message': amsgs.msgs[amsgs.UNAUTHORIZED_REQUEST]})
    test(svc_port, make_base_url(base_api.transactions.transaction_reset.location), 'PATCH', tku, {}, 400,
         {'message': amsgs.msgs[amsgs.MISSING_REQUEST_ARGUMENT]})

    test(svc_port, make_base_url(base_api.transactions.transaction_reset.location), 'PATCH', tku,
         {'id_user': dbuser1.id_user}, 204, {})

