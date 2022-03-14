-- Insert info data

BEGIN;
INSERT INTO servers.info VALUES
	(0, 'task_1', '192.168.1.100');
INSERT INTO tasks.update_info (time, server_id, task_configuration) VALUES
	('2022-03-14 10:56:43', 0, '{"param_1": "param_1_value", "param_2": "param_2_value"}'::json);
INSERT INTO modules.info (server_id, position, type) VALUES
    (0, 0, 'A'),
    (0, 1, 'A'),
    (0, 2, 'B');
INSERT INTO sockets.info (server_id, name, port, type) VALUES
	(0, 'data_socket', 4090, 'TCP'),
	(0, 'connect_socket', 4091, 'unix');
COMMIT;


BEGIN;
INSERT INTO servers.info VALUES
	(1, 'task_2', '192.168.1.101');
INSERT INTO tasks.update_info (time, server_id, task_configuration) VALUES
	('2022-03-14 10:56:51', 1, '{"param_1": "param_1_value", "param_2": "param_2_value", "param_3": 1}'::json);
INSERT INTO modules.info (server_id, position, type) VALUES
    (1, 0, 'A'),
    (1, 1, 'C'),
    (1, 2, 'B');
INSERT INTO sockets.info (server_id, name, port, type) VALUES
	(1, 'data_socket', 4090, 'TCP'),
	(1, 'connect_socket', 4091, 'unix'),
	(1, 'exchange_socket', 4190, 'unix');
COMMIT;


-- Insent statistic data

---- servers statistic

INSERT INTO servers.statistic (time, server_id, workload_percentage, temperature, RAM_used, disk_used) VALUES
	('2022-03-14 10:57:01', 0, 65.4, 23.1, 45567345, 945530968),
	('2022-03-14 10:57:01', 1, 43.9, 25.5, 85743658, 473847364);
COMMIT;

INSERT INTO servers.statistic (time, server_id, workload_percentage, temperature, RAM_used, disk_used) VALUES
	('2022-03-14 10:57:04', 0, 65.7, 23.2, 45597497, 945530968),
	('2022-03-14 10:57:04', 1, 47.3, 23.2, 85743645, 473847345);
COMMIT;

---- tasks statistic

INSERT INTO tasks.statistic (time, server_id, speed_in, speed_out, total_in, total_out, total_dropped) VALUES
	('2022-03-14 10:57:01', 0, 124, 100, 10975, 10874, 0),
    ('2022-03-14 10:57:01', 1, 73, 73, 693, 693, 0);
COMMIT;

INSERT INTO tasks.statistic (time, server_id, speed_in, speed_out, total_in, total_out, total_dropped) VALUES
	('2022-03-14 10:57:04', 0, 120, 128, 11163, 11154, 3),
    ('2022-03-14 10:57:04', 1, 77, 70, 840, 830, 0);
COMMIT;

---- modules statistic

INSERT INTO modules.statistic (time, module_id, status, message, data) VALUES
    ('2022-03-14 10:57:01', 1, 1, DEFAULT, '{"param_a": 1, "param_b": 2}'::json),
    ('2022-03-14 10:57:01', 2, 1, DEFAULT, '{"param_a": 11, "param_b": 22}'::json),
    ('2022-03-14 10:57:01', 3, 1, 'Warning: module warning', '{"param_c": "value", "param_d": 3}'::json),
    ('2022-03-14 10:57:01', 5, 0, 'Error: modules error', '{}'::json),
    ('2022-03-14 10:57:01', 6, 1, DEFAULT, '{"param_c": "value", "param_d": 10}'::json);
COMMIT;

INSERT INTO modules.statistic (time, module_id, status, message, data) VALUES
    ('2022-03-14 10:57:04', 1, 1, DEFAULT, '{"param_a": 5, "param_b": 4}'::json),
    ('2022-03-14 10:57:04', 2, 1, DEFAULT, '{"param_a": 23, "param_b": 64}'::json),
    ('2022-03-14 10:57:04', 3, 1, DEFAULT, '{"param_c": "new_value", "param_d": 53}'::json),
    ('2022-03-14 10:57:04', 4, 1, DEFAULT, '{"param_a": 2, "param_b": 3}'::json),
    ('2022-03-14 10:57:04', 5, 0, 'Error: modules error', '{}'::json),
    ('2022-03-14 10:57:04', 6, 1, 'Warning: error type', '{"param_c": "value", "param_d": 10}'::json);
COMMIT;

---- sockets statistic

INSERT INTO sockets.statistic (socket_id, time, status, direction, bytes_per_sec, packet_per_sec, 
    crashed_packet_per_sec, bytes_total, packets_total, crashed_packet_total) VALUES 
    (1, '2022-03-14 10:57:01', 'work', false, 15742853, 147, 0, 64325843, 684, 0),
    (1, '2022-03-14 10:57:01', 'work', true, 15357439, 139, 0, 63543859, 630, 0),
    (2, '2022-03-14 10:57:01', 'work', false, 6475839, 10, 0, 8475839, 80, 0),
    (2, '2022-03-14 10:57:01', 'work', true, 6045386, 9, 0, 8423554, 79, 1),
    (4, '2022-03-14 10:57:01', 'work', false, 1948765, 34, 1, 14437586, 114, 6),
    (4, '2022-03-14 10:57:01', 'work', true, 1546753, 9, 0, 12457843, 97, 0);
COMMIT;

INSERT INTO sockets.statistic (socket_id, time, status, direction, bytes_per_sec, packet_per_sec, 
    crashed_packet_per_sec, bytes_total, packets_total, crashed_packet_total) VALUES 
    (1, '2022-03-14 10:57:04', 'work', false, 4758365, 17, 0, 68573647, 700, 0),
    (1, '2022-03-14 10:57:04', 'work', true, 4038658, 13, 0, 66758475, 697, 0),
    (2, '2022-03-14 10:57:04', 'not work', false, 0, 0, 0, 8475839, 80, 0),
    (2, '2022-03-14 10:57:04', 'not work', true, 0, 0, 0, 8423554, 79, 1),
    (4, '2022-03-14 10:57:04', 'error', false, 0, 0, 165, 14437586, 114, 534),
    (4, '2022-03-14 10:57:04', 'warning', true, 14653, 9, 25, 12448593, 97, 376),
    (5, '2022-03-14 10:57:04', 'warning', false, 1398, 1, 3, 2374, 3, 9);
COMMIT;

---- sockets alarms

INSERT INTO sockets.alarm (socket_id, time, name, type, message) VALUES 
    (4, '2022-03-14 10:57:04', 'Port error', 'system alarm', 'Text of error'),
    (4, '2022-03-14 10:57:04', 'Warning', 'local alarm', 'Text of warning'),
    (5, '2022-03-14 10:57:04', 'Warning', 'local alarm', 'Text of warning');
COMMIT;



