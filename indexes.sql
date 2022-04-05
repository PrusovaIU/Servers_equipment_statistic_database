--tasks update indexes

CREATE INDEX IF NOT EXISTS ix_tasks_update_info_server_id ON tasks.update_info(server_id);
COMMIT;
EXPLAIN SELECT updates.server_id, MAX(updates.time)
    FROM tasks.update_info as updates
    WHERE updates.server_id BETWEEN 0 AND 5
    GROUP BY updates.server_id
    ORDER BY updates.server_id;
                                               QUERY PLAN                                                
---------------------------------------------------------------------------------------------------------
 GroupAggregate  (cost=12.75..12.83 rows=5 width=12)
   Group Key: server_id
   ->  Sort  (cost=12.75..12.76 rows=5 width=12)
         Sort Key: server_id
         ->  Bitmap Heap Scan on update_info updates  (cost=4.20..12.69 rows=5 width=12)
               Recheck Cond: ((server_id >= 0) AND (server_id <= 5))
               ->  Bitmap Index Scan on ix_tasks_update_info_server_id  (cost=0.00..4.20 rows=5 width=0)
                     Index Cond: ((server_id >= 0) AND (server_id <= 5))


--modules info indexes

----ON server_id

CREATE INDEX IF NOT EXISTS ix_modules_info_server_id ON modules.info(server_id);
COMMIT;
EXPLAIN SELECT ARRAY_AGG(module_id), module_type FROM modules.info 
	WHERE server_id=1
	GROUP BY module_type;
                                          QUERY PLAN                                          
----------------------------------------------------------------------------------------------
 HashAggregate  (cost=2.87..2.94 rows=5 width=34)
   Group Key: module_type
   ->  Index Scan using ix_modules_info_server_id on info  (cost=0.15..2.82 rows=10 width=6)
         Index Cond: (server_id = 1)
		 
----ON module type

CREATE INDEX IF NOT EXISTS ix_modules_module_type ON modules.info USING GIN (to_tsvector('english', module_type));
COMMIT;
EXPLAIN SELECT server_id, 
    ARRAY_AGG(module_id) AS modules_ids, 
    ARRAY_AGG(position) AS positions
    FROM modules.info 
    WHERE to_tsvector('english', module_type) @@ to_tsquery('english', 'D')
    GROUP BY server_id
    ORDER BY server_id;
                                              QUERY PLAN                                              
------------------------------------------------------------------------------------------------------
 GroupAggregate  (cost=4.03..4.06 rows=1 width=68)
   Group Key: server_id
   ->  Sort  (cost=4.03..4.04 rows=1 width=12)
         Sort Key: server_id
         ->  Bitmap Heap Scan on info  (cost=2.51..4.02 rows=1 width=12)
               Recheck Cond: (to_tsvector('english'::regconfig, module_type) @@ '''d'''::tsquery)
               ->  Bitmap Index Scan on ix_modules_module_type  (cost=0.00..2.51 rows=1 width=0)
                     Index Cond: (to_tsvector('english'::regconfig, module_type) @@ '''d'''::tsquery)
					 
----ON server_id, position
CREATE UNIQUE INDEX ix_module_info_server_id_position ON modules.info(server_id, position);
COMMIT;
					 

--sockets info indexes

----ON server_id

CREATE INDEX IF NOT EXISTS ix_sockets_info_server_id ON sockets.info(server_id);
COMMIT;
EXPLAIN SELECT sockets.socket_id, sockets.port, sockets.socket_type 
    FROM sockets.info AS sockets
    WHERE sockets.server_id BETWEEN 3 AND 10;
                                       QUERY PLAN                                       
----------------------------------------------------------------------------------------
 Bitmap Heap Scan on info sockets  (cost=4.19..12.66 rows=4 width=40)
   Recheck Cond: ((server_id >= 3) AND (server_id <= 10))
   ->  Bitmap Index Scan on ix_sockets_info_server_id  (cost=0.00..4.19 rows=4 width=0)
         Index Cond: ((server_id >= 3) AND (server_id <= 10))


----ON socket_type

CREATE INDEX IF NOT EXISTS ix_sockets_info_socket_type ON sockets.info USING GIN (to_tsvector('english', socket_type));
COMMIT;
EXPLAIN SELECT sockets.server_id, servers_info.host, 
    ARRAY_AGG(sockets.socket_id) AS sockets_ids, 
    ARRAY_AGG(sockets.port) AS sockets_ports
    FROM sockets.info AS sockets
    INNER JOIN servers.info AS servers_info ON sockets.server_id = servers_info.server_id
    WHERE to_tsvector('english', sockets.socket_type) @@  to_tsquery('english', 'net1')
    GROUP BY sockets.server_id, servers_info.host
    ORDER BY sockets.server_id;
                                                  QUERY PLAN                                                   
---------------------------------------------------------------------------------------------------------------
 GroupAggregate  (cost=6.70..6.73 rows=1 width=116)
   Group Key: sockets.server_id, servers_info.host
   ->  Sort  (cost=6.70..6.71 rows=1 width=60)
         Sort Key: sockets.server_id, servers_info.host
         ->  Nested Loop  (cost=2.65..6.69 rows=1 width=60)
               ->  Bitmap Heap Scan on info sockets  (cost=2.50..4.02 rows=1 width=12)
                     Recheck Cond: (to_tsvector('english'::regconfig, socket_type) @@ '''net1'''::tsquery)
                     ->  Bitmap Index Scan on ix_sockets_info_socket_type  (cost=0.00..2.50 rows=1 width=0)
                           Index Cond: (to_tsvector('english'::regconfig, socket_type) @@ '''net1'''::tsquery)
               ->  Index Scan using info_pkey on info servers_info  (cost=0.15..2.67 rows=1 width=52)
                     Index Cond: (server_id = sockets.server_id)
					 
----ON server_id-port
CREATE UNIQUE INDEX ix_sockets_info_server_id_port ON sockets.info(server_id, port);
COMMIT;


--sockets alarms indexes

----ON alarm_type

CREATE INDEX ix_sockets_alarm_alarm_type IF NOT EXISTS ON sockets.alarm USING GIN (to_tsvector('english', alarm_type));
COMMIT;
EXPLAIN SELECT * FROM sockets.alarm
    WHERE to_tsvector('english', alarm_type) @@ to_tsquery('english', 'warning');
	                                         QUERY PLAN                                         
--------------------------------------------------------------------------------------------
 Bitmap Heap Scan on alarm  (cost=2.53..6.61 rows=3 width=57)
   Recheck Cond: (to_tsvector('english'::regconfig, alarm_type) @@ '''warn'''::tsquery)
   ->  Bitmap Index Scan on ix_sockets_alarm_alarm_type  (cost=0.00..2.53 rows=3 width=0)
         Index Cond: (to_tsvector('english'::regconfig, alarm_type) @@ '''warn'''::tsquery)




