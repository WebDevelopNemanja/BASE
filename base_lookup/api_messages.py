# -*- coding: utf-8 -*-

EXCEPTION = 1
OK = 2
USERNAME_ALREADY_TAKEN = 10
USER_NOT_FOUND = 11
USER_PASSWORD_CHANGED = 12
UNAUTHORIZED_REQUEST = 13
CLOSE_USER_SESSION = 14
DATA_SOURCE_NOT_DEFINED = 15
MISSING_REQUEST_ARGUMENT = 16
PASSWORD_TOKEN_EXPIRED = 17
USER_PASSWORD_CHANGE_ERROR = 18
CANNOT_SAVE_MESSAGE = 19
MESSAGE_SAVED = 20
WRONG_PASSWORD = 21
INVALID_PASSWORD = 22
ERROR_SERIALIZE_USER = 23
ERROR_REGISTER_USER = 24
ERROR_LOGIN_USER = 25
INVALID_REQUEST_ARGUMENT = 26
NOT_IMPLEMENTED_GET = 27
NOT_IMPLEMENTED_PUT = 28
NOT_IMPLEMENTED_POST = 29
NOT_IMPLEMENTED_DELETE = 30
WRONG_USERNAME_OR_PASSWORD = 31
CHANGE_USERNAME_REQUEST = 32
WRONG_OR_EXPIRED_TOKEN = 33
TOKEN_MISSING_ARGUMENT = 34
USER_UPDATE_ERROR = 35
USER_NAME_CHANGED = 36
REQUEST_NOT_ALLOWED = 37
NOT_FOUND_IN_DB = 38
ERROR_SAVE_HASH = 39
ERROR_RETRIEVE_HASH = 40
MISSING_URL_HASH = 41
USER_NOT_ACTIVE = 42
ERROR_POST_REGISTRATION = 43
API_CALL_EXCEPTION = 44
NOT_API_CALL = 45
NOT_IMPLEMENTED_PATCH = 46
ERROR_POST_LOGIN = 47
ERROR_SET_OPTION = 48
ERROR_GET_OPTION = 49
OPTION_NOT_EXIST = 50
ERROR_UPDATE_MESSAGE = 51
ERROR_POST_CHECK = 52
ERROR_PACK_LOOKUPS = 53
SQL_QUERY_ERROR = 54
ERROR_CHANGE_USERNAME = 55
MISSING_REDIRECTION_URL = 56
ERROR_PASSWORD_RESTORE = 57
INVALID_HASH_DATA = 58
CLUB_NOT_FOUND = 59
HEAD_COACH_NOT_FOUND = 60

msgs = {}
msgs[EXCEPTION] = "Exception"
msgs[OK] = "OK"
msgs[USERNAME_ALREADY_TAKEN] = "User name is already taken"
msgs[USER_NOT_FOUND] = "Wrong username/password"
msgs[USER_PASSWORD_CHANGED] = "Password changed"
msgs[UNAUTHORIZED_REQUEST] = "Unauthorized request"
msgs[CLOSE_USER_SESSION] = "Close session"
msgs[DATA_SOURCE_NOT_DEFINED] = "Data source not defined"
msgs[MISSING_REQUEST_ARGUMENT] = "Missing request argument"
msgs[PASSWORD_TOKEN_EXPIRED] = "User not found or user token expired"
msgs[USER_PASSWORD_CHANGE_ERROR] = "Error change users password"
msgs[CANNOT_SAVE_MESSAGE] = "Cannot save message"
msgs[MESSAGE_SAVED] = "Message saved"
msgs[WRONG_PASSWORD] = "Wrong password"
msgs[INVALID_PASSWORD] = "Password format invalid"
msgs[ERROR_SERIALIZE_USER] = "Error serializing user"
msgs[ERROR_REGISTER_USER] = "Error register user"
msgs[ERROR_LOGIN_USER] = "Error login user"
msgs[INVALID_REQUEST_ARGUMENT] = "Invalid request argument"
msgs[NOT_IMPLEMENTED_DELETE] = "DELETE not implemented"
msgs[NOT_IMPLEMENTED_GET] = "GET not implemented"
msgs[NOT_IMPLEMENTED_PUT] = "PUT not implemented"
msgs[NOT_IMPLEMENTED_POST] = "POST not implemented"
msgs[NOT_IMPLEMENTED_PATCH] = "PATCH not implemented"
msgs[WRONG_USERNAME_OR_PASSWORD] = "Wrong username or password"
msgs[CHANGE_USERNAME_REQUEST] = "User requested username change"
msgs[WRONG_OR_EXPIRED_TOKEN] = "Token is not correct or expired"
msgs[TOKEN_MISSING_ARGUMENT] = "Missing argument in token"
msgs[USER_UPDATE_ERROR] = "Error updating user"
msgs[USER_NAME_CHANGED] = "Username changed"
msgs[REQUEST_NOT_ALLOWED] = "Request not allowed"
msgs[NOT_FOUND_IN_DB] = "Not found"
msgs[ERROR_SAVE_HASH] = "Error save hash"
msgs[ERROR_RETRIEVE_HASH] = "Wrong url used"
msgs[MISSING_URL_HASH] = "Missing url parameter"
msgs[USER_NOT_ACTIVE] = "User is not active"
msgs[ERROR_POST_REGISTRATION] = "Post registration error"
msgs[API_CALL_EXCEPTION] = "Call Error"
msgs[NOT_API_CALL] = "Error execute method"
msgs[ERROR_POST_LOGIN] = "Post login error"
msgs[ERROR_SET_OPTION] = "Error setting option"
msgs[ERROR_GET_OPTION] = "Error getting option"
msgs[OPTION_NOT_EXIST] = "Option does not exists"
msgs[ERROR_UPDATE_MESSAGE] = "Error update mail queue"
msgs[ERROR_POST_CHECK] = "Check post error"
msgs[ERROR_PACK_LOOKUPS] = "Error pack lookups"
msgs[SQL_QUERY_ERROR] = "SQL Query error"
msgs[ERROR_CHANGE_USERNAME] = "Change username error"
msgs[MISSING_REDIRECTION_URL] = "Missing redirection url"
msgs[ERROR_PASSWORD_RESTORE] = "Forget password error"
msgs[INVALID_HASH_DATA] = "Invalid hash data"
msgs[CLUB_NOT_FOUND] = "Club not found"
msgs[HEAD_COACH_NOT_FOUND] = "Head coach not found"
