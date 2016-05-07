CREATE TABLE IF NOT EXISTS auth_users (
	id char(10) PRIMARY KEY,
	username varchar(128) NOT NULL UNIQUE,
	password char(255) NOT NULL,
	password_expire DATETIME,
	active BOOLEAN NOT NULL DEFAULT FALSE,
	role_flags int NOT NULL,
	INDEX (username),
	INDEX (active),
	INDEX (role_flags)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS balanced_servers (
	id bigint NOT NULL AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(32) UNIQUE NOT NULL,
  ip VARCHAR(128) NOT NULL,
	port VARCHAR(10) NOT NULL,
	created DATETIME NOT NULL,
	deactivated DATETIME,
	active BOOLEAN NOT NULL,
  INDEX (name),
	INDEX (ip),
	INDEX (active),
	UNIQUE KEY balanced_server_uk0 (ip, port)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE users_server (
	id_user char(10) UNIQUE NOT NULL,
	id_server bigint NOT NULL,
	CONSTRAINT users_server_fk0 FOREIGN KEY (id_user) REFERENCES auth_users(id),
	CONSTRAINT users_server_fk1 FOREIGN KEY (id_server) REFERENCES balanced_servers(id),
	UNIQUE KEY users_server_uk1 (id_user, id_server)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE hash_2_params (
	id bigint NOT NULL AUTO_INCREMENT PRIMARY KEY,
	hash char(64) NOT NULL UNIQUE,
	time_created DATETIME NOT NULL,
	time_to_live int,
	expire_after_first_access BOOLEAN NOT NULL DEFAULT FALSE,
	last_access DATETIME,
	data TEXT NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE hash_2_params_historylog (
	id bigint NOT NULL AUTO_INCREMENT PRIMARY KEY,
	id_hash_2_params bigint NOT NULL,
	ip varchar(16) NOT NULL,
	log_time DATETIME NOT NULL,
	CONSTRAINT hash_2_params_historylog_fk0 FOREIGN KEY (id_hash_2_params) REFERENCES hash_2_params(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS sequencers (
	id char(2) NOT NULL,
	s_partition char(2) NOT NULL,
	size smallint NOT NULL,
	active_stage char(3) NOT NULL,
	check_sum_size smallint NOT NULL,
	name varchar(16) NOT NULL UNIQUE,
	type varchar(16) NOT NULL,
	s_table varchar(32) NOT NULL UNIQUE,
	ordered BOOLEAN NOT NULL DEFAULT FALSE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE IF NOT EXISTS options(
	id bigint NOT NULL AUTO_INCREMENT PRIMARY KEY,
  o_key VARCHAR(32) NOT NULL,
  o_value VARCHAR(128) NOT NULL,
  INDEX (o_key)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


-- SESSION TOKENS --

DROP TABLE IF EXISTS session_token;
CREATE TABLE session_token (
  id char(64) PRIMARY KEY,
  id_user char(10) NOT NULL,
  created DATETIME NOT NULL,
	expiration DATETIME,
	inactive_expiration int,
  closed boolean DEFAULT FALSE,
	INDEX (id_user),
	INDEX (closed),
	CONSTRAINT session_token_fk0 FOREIGN KEY (id_user) REFERENCES auth_users(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE mail_queue (
	id bigint NOT NULL AUTO_INCREMENT PRIMARY KEY,
	sender varchar(128) NOT NULL,
	receiver TEXT NOT NULL,
	time_created DATETIME NOT NULL,
	time_sent DATETIME,
	sent BOOLEAN NOT NULL DEFAULT FALSE,
	message TEXT NOT NULL,
	data TEXT,
	INDEX email_sender_idx (sender),
	INDEX email_sent (sent)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

insert into sequencers (id, s_partition, active_stage, size, check_sum_size, name ,type, s_table, ordered)
values
('a','00','000',4,0,'auth_users','STR','s_auth_users',false),
('s','00','000',58,0,'session_token','STR','s_session_token',false),
('h','00','000',58,0,'hash_2_params','STR','s_hash_2_params ',false),
('t','00','000',10,0,'transactions','STR','s_transactions',false),
('v','00','000',4,0,'account_summary','STR','s_account_summary',false),
('w','00','000',4,0,'daily_summary','STR','s_daily_summary',false);

drop table if exists s_auth_users;
CREATE TABLE s_auth_users (
    id char(10) PRIMARY KEY,
    active_stage char(3)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

drop table if exists s_session_token;
CREATE TABLE s_session_token (
    id char(64) PRIMARY KEY,
    active_stage char(3)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

drop table if exists s_hash_2_params ;
CREATE TABLE s_hash_2_params (
	id char(64) PRIMARY KEY,
	active_stage char(3)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

drop table if exists s_transactions;
CREATE TABLE s_transactions(
    id char(16) PRIMARY KEY,
    active_stage char(3)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

drop table if exists s_account_summary;
CREATE TABLE s_account_summary(
	id char(10) PRIMARY KEY,
	active_stage char(3)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

drop table if exists s_daily_summary;
CREATE TABLE s_daily_summary(
	id char(10) PRIMARY KEY,
	active_stage char(3)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- TRANSACTIONS --
CREATE TABLE IF NOT EXISTS currency(
	id INTEGER PRIMARY KEY AUTO_INCREMENT,
	currency char(3) NOT NULL,
	last_modified DATETIME NOT NULL DEFAULT NOW(),
	value DECIMAL(10,2) NOT NULL,
	INDEX (currency)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO currency (currency, value) VALUES ('EUR', 1.00);

CREATE TABLE IF NOT EXISTS transactions(
	id char(16) PRIMARY KEY,
	id_user char(10) NOT NULL,
	transaction_time DATETIME(4) NOT NULL,
	transaction_type int NOT NULL,
	value DECIMAL(10,2) NOT NULL,
	referent_value DECIMAL(10,2) NOT NULL,
	id_currency_change INTEGER NOT NULL,
	data text,
	INDEX (id_user),
	INDEX (transaction_type ),
	CONSTRAINT transactions_fk0 FOREIGN KEY (id_user) REFERENCES auth_users(id),
	CONSTRAINT transactions_fk1 FOREIGN KEY (id_currency_change ) REFERENCES currency(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS account_summary(
	id char(10) PRIMARY KEY,
	id_user char(10) NOT NULL,
	balance DECIMAL(10,2) NOT NULL,
	payin_sum DECIMAL(10,2) NOT NULL,
	id_currency_change INTEGER NOT NULL,
	reset_time DATETIME(4),
	id_reset_user char(10),
	INDEX (id_user),
	INDEX (id_reset_user),
	INDEX (reset_time),
	CONSTRAINT account_summary_fk0 FOREIGN KEY (id_user) REFERENCES auth_users(id),
	CONSTRAINT account_summary_fk1 FOREIGN KEY (id_reset_user) REFERENCES auth_users(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS daily_summary(
	id char(10) PRIMARY KEY,
	id_user char(10) NOT NULL,
	date DATE NOT NULL,
	summary DECIMAL(10,2) NOT NULL,
	id_currency_change INTEGER NOT NULL,
	reset_time DATETIME(4),
	id_reset_user char(10),
	INDEX (id_user),
	INDEX (id_reset_user),
	INDEX (reset_time),
	INDEX (date),
	CONSTRAINT daily_summary_fk0 FOREIGN KEY (id_user) REFERENCES auth_users(id),
	CONSTRAINT daily_summary_fk1 FOREIGN KEY (id_reset_user) REFERENCES auth_users(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;




