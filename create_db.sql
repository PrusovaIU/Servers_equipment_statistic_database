CREATE ROLE ses_source LOGIN;

CREATE SCHEMA IF NOT EXISTS servers;

GRANT CREATE, USAGE ON SCHEMA servers TO ses_source;

CREATE TABLE IF NOT EXISTS servers.info
(
    id integer PRIMARY KEY NOT NULL,
    update_time time zone NOT NULL,
    task text NOT NULL
);

CREATE TABLE IF NOT EXISTS servers.statistic
(
	id SERIAL PRIMARY KEY,
	time time NOT NULL,
	server_id integer REFERENCES servers.info (id),
	workload_percentage real CHECK (workload_percentage >= 0),
	temperature real,
	RAM_used real CHECK (RAM_used >= 0),
	disk_used real CHECK (disk_used >= 0)
);

CREATE SCHEMA IF NOT EXISTS tasks;

GRANT CREATE, USAGE ON SCHEMA tasks TO ses_source;

CREATE TABLE IF NOT EXISTS tasks.update_info
(
	id SERIAL PRIMARY KEY,
	time time NOT NULL,
	server_id integer REFERENCES servers.info (id),
	task_configuration json NOT NULL
);

CREATE TABLE IF NOT EXISTS tasks.statistic
(
	id SERIAL PRIMARY KEY,
	time time NOT NULL,
	server_id integer REFERENCES servers.info (id),
	speed_in integer CHECK (speed_in >= 0),
	speed_out integer CHECK (speed_out >= 0),
	total_in integer CHECK (total_in >= 0),
	total_out integer CHECK (total_out >= 0),
	total_dropped integer CHECK (total_dropped >= 0)
);

CREATE SCHEMA IF NOT EXISTS modules;

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
	time time NOT NULL,
	module_id integer REFERENCES modules.info (id),
	status integer NOT NULL,
	message text,
	data jsonb
);

CREATE SCHEMA IF NOT EXISTS sockets;

CREATE TABLE IF NOT EXISTS sockets.info
(
	id integer PRIMARY KEY NOT NULL,
	server_id integer REFERENCES servers.info (id),
	name text NOT NULL,
	host varchar(15) NOT NULL,
	port integer NOT NULL,
	type text NOT NULL
);


