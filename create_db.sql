CREATE ROLE ses_source LOGIN;
CREATE ROLE ses_reader LOGIN;

CREATE SCHEMA IF NOT EXISTS servers;

GRANT CREATE, USAGE ON SCHEMA servers TO ses_source;
GRANT USAGE ON SCHEMA servers TO ses_reader;

CREATE TABLE IF NOT EXISTS servers.info
(
    server_id integer PRIMARY KEY NOT NULL,
    task text NOT NULL,
	host varchar(15) NOT NULL
);

CREATE TABLE IF NOT EXISTS servers.statistic
(
	record_id SERIAL PRIMARY KEY,
	time timestamp NOT NULL,
	server_id integer REFERENCES servers.info (server_id) NOT NULL,
	workload_percentage real CHECK (workload_percentage >= 0),
	temperature real,
	ram_used bigint CHECK (ram_used >= 0),
	disk_used bigint CHECK (disk_used >= 0)
);

COMMIT;

CREATE SCHEMA IF NOT EXISTS tasks;

GRANT CREATE, USAGE ON SCHEMA tasks TO ses_source;
GRANT USAGE ON SCHEMA tasks TO ses_reader;

CREATE TABLE IF NOT EXISTS tasks.update_info
(
	record_id SERIAL PRIMARY KEY,
	time timestamp NOT NULL,
	server_id integer REFERENCES servers.info (server_id) NOT NULL,
	task_configuration json NOT NULL
);

CREATE TABLE IF NOT EXISTS tasks.statistic
(
	record_id SERIAL PRIMARY KEY,
	time timestamp NOT NULL,
	server_id integer REFERENCES servers.info (server_id) NOT NULL,
	speed_in bigint CHECK (speed_in >= 0),
	speed_out bigint CHECK (speed_out >= 0),
	total_in bigint CHECK (total_in >= 0),
	total_out bigint CHECK (total_out >= 0),
	total_dropped bigint CHECK (total_dropped >= 0)
);

COMMIT;

CREATE SCHEMA IF NOT EXISTS modules;

GRANT CREATE, USAGE ON SCHEMA modules TO ses_source;
GRANT USAGE ON SCHEMA modules TO ses_reader;

CREATE TABLE IF NOT EXISTS modules.info
(
	module_id SERIAL PRIMARY KEY,
	server_id integer REFERENCES servers.info (server_id) NOT NULL,
	position integer NOT NULL CHECK (position >= 0),
	type text NOT NULL
);

CREATE TABLE IF NOT EXISTS modules.statistic
(
	record_id SERIAL PRIMARY KEY,
	time timestamp NOT NULL,
	module_id integer REFERENCES modules.info (module_id) NOT NULL,
	status integer NOT NULL,
	message text DEFAULT '',
	data jsonb
);

COMMIT;

CREATE SCHEMA IF NOT EXISTS sockets;

GRANT CREATE, USAGE ON SCHEMA sockets TO ses_source;
GRANT USAGE ON SCHEMA sockets TO ses_reader;

CREATE TABLE IF NOT EXISTS sockets.info
(
	socket_id SERIAL PRIMARY KEY,
	server_id integer REFERENCES servers.info (server_id) NOT NULL,
	name text NOT NULL,
	port integer NOT NULL CHECK (port >= 0),
	type text NOT NULL
);

CREATE TABLE IF NOT EXISTS sockets.statistic
(
	record_id serial PRIMARY KEY,
	socket_id integer REFERENCES sockets.info (socket_id) NOT NULL,
	time timestamp NOT NULL,
	status text NOT NULL,
	direction boolean NOT NULL,
	bytes_per_sec bigint CHECK (bytes_per_sec >= 0),
	packet_per_sec bigint CHECK (packet_per_sec >= 0),
	crashed_packet_per_sec bigint CHECK (crashed_packet_per_sec >= 0),
	bytes_total bigint CHECK (bytes_total >= 0),
	packets_total bigint CHECK (packets_total >= 0),
	crashed_packet_total bigint CHECK (crashed_packet_total >= 0)
);

CREATE TABLE IF NOT EXISTS sockets.alarm
(
	record_id serial PRIMARY KEY,
	socket_id integer REFERENCES sockets.info (socket_id) NOT NULL,
	time timestamp NOT NULL,
	name text NOT NULL,
	type text NOT NULL,
	message text DEFAULT ''
);

COMMIT;
