"""
Application specific hooks will be added to this module, or
existing will be overloaded if needed

format_password -- format password for new user (parameters: username, password)
check_password -- check password is right (parameters: password from db, username, password)
check_users_data_is_valid -- check data for user registration is valid (username, password, json users data)
choose_balanced_server -- choose balanced server algorithm
get_user_id -- get id for new user (username, password, json users data)
check_password_is_valid -- validate given password (parameters: password) (user_register)
post_register_digest -- post register users data processing
                        (parameters: users id, username, password, json users data) (user_register)
prepare_user_query -- prepare query for insert user in db
                        (parameters: request handler, users id, username, password, json users data) (user_register)
pack_user_by_id -- get user from db by it's id (db connection, user id) (dbtokens)
prepare_login_query -- prepare query for user login (parameters: username)
post_login_digest -- post login processing (parameters: id_user, username, password(plain), login token)
"""

import bcrypt
from base_config.service import log
from base_common.seq import sequencer
from base_common.dbacommon import get_balanced_servers


def choose_balanced_server():

    _servers = get_balanced_servers()
    import random
    _chosen_id = random.choice([s_id for s_id in _servers])
    _chosen = _servers[_chosen_id]
    _chosen['id'] = _chosen_id
    return _chosen


def format_password(username, password):

    return bcrypt.hashpw('{}{}'.format(username, password).encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def check_password(db_pwd, username, password):

    pwd = '{}{}'.format(username, password).encode('utf-8')
    dpwd = db_pwd.encode('utf-8')
    return dpwd == bcrypt.hashpw(pwd, dpwd)


def get_user_id(username, password, user_data):

    return sequencer().new('a')


def prepare_user_query(u_id, username, password, *args, **kwargs):
    """
    User registration query
    :param u_id:  user's id (unique)
    :param username:  user's username
    :param password:  given password
    :param args:  additional arguments (application specific)
    :param kwargs:  additional named arguments (application specific)
    :return:
    """

    password = format_password(username, password)

    # role_flags - HARDCODED to 1

    q = "INSERT into auth_users (id, username, password, role_flags, active) VALUES " \
        "('{}', '{}', '{}', 1, true)".format(
                u_id,
                username,
                password)

    return q


def pack_user_by_id(db, id_user, get_dict=False):
    """
    Pack users information in DBUser class instance
    :param db: database
    :param id_user: users id
    :param get_dict: export user like DBUser or dict
    :return: DBUser instance or user dict
    """

    dbc = db.cursor()
    q = "select id, username, password, role_flags, active from auth_users where id = '{}'".format(id_user)

    import MySQLdb
    try:
        dbc.execute(q)
    except MySQLdb.IntegrityError as e:
        log.critical('Error find user by token: {}'.format(e))
        return False

    if dbc.rowcount != 1:
        log.critical('Fount {} auth_users with id {}'.format(dbc.rowcount, id_user))
        return False

    #DUMMY CLASS INSTANCE USER JUST FOR EASIER MANIPULATION OF DATA
    class DBUser:

        def dump_user(self):
            ret = {}
            for k in self.__dict__:
                if self.__dict__[k]:
                    ret[k] = self.__dict__[k]

            return ret

    db_user = DBUser()

    user = dbc.fetchone()
    db_user.id_user = user['id']
    db_user.username = user['username']
    db_user.password = user['password']
    db_user.role = user['role_flags']
    db_user.active = user['active']

    return db_user.dump_user() if get_dict else db_user


def prepare_login_query(username):

    q = "select id, password from auth_users where username = '{}'".format( username )

    return q

