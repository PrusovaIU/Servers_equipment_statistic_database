CREATE ROLE ses_source LOGIN;
CREATE ROLE ses_reader LOGIN;

CREATE SCHEMA IF NOT EXISTS servers;

GRANT CREATE, USAGE ON SCHEMA servers TO ses_source;
GRANT USAGE ON SCHEMA servers TO ses_reader;

CREATE TABLE IF NOT EXISTS servers.info
(
    id integer PRIMARY KEY NOT NULL,
    task text NOT NULL,
	host varchar(15) NOT NULL
);

CREATE TABLE IF NOT EXISTS servers.statistic
(
	id SERIAL PRIMARY KEY,
	time timestamp NOT NULL,
	server_id integer REFERENCES servers.info (id),
	workload_percentage real CHECK (workload_percentage >= 0),
	temperature real,
	RAM_used integer CHECK (RAM_used >= 0),
	disk_used integer CHECK (disk_used >= 0)
);

COMMIT;

CREATE SCHEMA IF NOT EXISTS tasks;

GRANT CREATE, USAGE ON SCHEMA tasks TO ses_source;
GRANT USAGE ON SCHEMA tasks TO ses_reader;

CREATE TABLE IF NOT EXISTS tasks.update_info
(
	id SERIAL PRIMARY KEY,
	time timestamp NOT NULL,
	server_id integer REFERENCES servers.info (id),
	task_configuration json NOT NULL
);

CREATE TABLE IF NOT EXISTS tasks.statistic
(
	id SERIAL PRIMARY KEY,
	time timestamp NOT NULL,
	server_id integer REFERENCES servers.info (id),
	speed_in integer CHECK (speed_in >= 0),
	speed_out integer CHECK (speed_out >= 0),
	total_in integer CHECK (total_in >= 0),
	total_out integer CHECK (total_out >= 0),
	total_dropped integer CHECK (total_dropped >= 0)
);

COMMIT;

CREATE SCHEMA IF NOT EXISTS modules;

GRANT CREATE, USAGE ON SCHEMA modules TO ses_source;
GRANT USAGE ON SCHEMA modules TO ses_reader;

CREATE TABLE IF NOT EXISTS modules.info
(
	id SERIAL PRIMARY KEY,
	server_id integer REFERENCES servers.info (id),
	position integer NOT NULL CHECK (position >= 0),
	type text NOT NULL
);

CREATE TABLE IF NOT EXISTS modules.statistic
(
	id SERIAL PRIMARY KEY,
	time timestamp NOT NULL,
	module_id integer REFERENCES modules.info (id),
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
	id SERIAL PRIMARY KEY,
	server_id integer REFERENCES servers.info (id),
	name text NOT NULL,
	port integer NOT NULL,
	type text NOT NULL
);

CREATE TABLE IF NOT EXISTS sockets.statistic
(
	id serial PRIMARY KEY,
	socket_id integer REFERENCES sockets.info (id),
	time timestamp NOT NULL,
	status text NOT NULL,
	direction boolean NOT NULL,
	bytes_per_sec integer CHECK (bytes_per_sec >= 0),
	packet_per_sec integer CHECK (packet_per_sec >= 0),
	crashed_packet_per_sec integer CHECK (crashed_packet_per_sec >= 0),
	bytes_total integer CHECK (bytes_total >= 0),
	packets_total integer CHECK (packets_total >= 0),
	crashed_packet_total integer CHECK (crashed_packet_total >= 0)
);

CREATE TABLE IF NOT EXISTS sockets.alarm
(
	id serial PRIMARY KEY,
	socket_id integer REFERENCES sockets.info (id),
	time timestamp NOT NULL,
	name text NOT NULL,
	type text NOT NULL,
	message text DEFAULT ''
);

COMMIT;
