--tasks update indexes

CREATE INDEX IF NOT EXISTS tasks_updates_server_id_idx ON tasks.update_info(server_id);
COMMIT;
EXPLAIN SELECT updates.server_id, MAX(updates.time), servers.info.host
    FROM tasks.update_info as updates
    INNER JOIN servers.info ON updates.server_id = servers.info.server_id
    WHERE updates.server_id BETWEEN 0 AND 5
    GROUP BY updates.server_id, servers.info.host
    ORDER BY updates.server_id;
                                    QUERY PLAN                                     
-----------------------------------------------------------------------------------
 HashAggregate  (cost=7.18..7.23 rows=5 width=60)
   Group Key: updates.server_id, info.host
   ->  Nested Loop  (cost=0.15..7.14 rows=6 width=60)
         ->  Index Scan using info_pkey on info  (cost=0.15..2.67 rows=1 width=52)
               Index Cond: (server_id = 0)
         ->  Seq Scan on update_info updates  (cost=0.00..4.41 rows=6 width=12)
               Filter: (server_id = 0)


--modules info indexes

----ON server_id

CREATE INDEX IF NOT EXISTS modules_info_server_id_idx ON modules.info(server_id);
COMMIT;
EXPLAIN SELECT ARRAY_AGG(module_id), module_type FROM modules.info 
	WHERE server_id=1
	GROUP BY module_type;
                                          QUERY PLAN                                          
----------------------------------------------------------------------------------------------
 HashAggregate  (cost=2.87..2.94 rows=5 width=34)
   Group Key: module_type
   ->  Index Scan using modules_info_server_id_idx on info  (cost=0.15..2.82 rows=10 width=6)
         Index Cond: (server_id = 1)
		 
----ON module type

CREATE INDEX IF NOT EXISTS module_type_idx ON modules.info USING GIN (to_tsvector('english', module_type));
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
               ->  Bitmap Index Scan on module_type_idx  (cost=0.00..2.51 rows=1 width=0)
                     Index Cond: (to_tsvector('english'::regconfig, module_type) @@ '''d'''::tsquery)
					 
----ON server_id, position
CREATE UNIQUE INDEX ON modules.info(server_id, position);
COMMIT;
					 

--sockets info indexes

----ON server_id

CREATE INDEX IF NOT EXISTS socket_info_server_id_idx ON sockets.info(server_id);
COMMIT;
EXPLAIN SELECT sockets.socket_id, servers_info.host, sockets.port, sockets.socket_type 
    FROM sockets.info AS sockets
    INNER JOIN servers.info AS servers_info ON sockets.server_id = servers_info.server_id
    WHERE sockets.server_id BETWEEN 3 AND 10;
                                        QUERY PLAN                                        
------------------------------------------------------------------------------------------
 Nested Loop  (cost=0.15..25.45 rows=48 width=61)
   ->  Seq Scan on info sockets  (cost=0.00..2.41 rows=48 width=17)
         Filter: ((server_id > 3) AND (server_id < 10))
   ->  Index Scan using info_pkey on info servers_info  (cost=0.15..0.48 rows=1 width=52)
         Index Cond: (server_id = sockets.server_id)

----ON socket_type

CREATE INDEX IF NOT EXISTS socket_type_idx ON sockets.info USING GIN (to_tsvector('english', socket_type));
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
                     ->  Bitmap Index Scan on socket_type_idx  (cost=0.00..2.50 rows=1 width=0)
                           Index Cond: (to_tsvector('english'::regconfig, socket_type) @@ '''net1'''::tsquery)
               ->  Index Scan using info_pkey on info servers_info  (cost=0.15..2.67 rows=1 width=52)
                     Index Cond: (server_id = sockets.server_id)
					 
----ON server_id-port
CREATE UNIQUE INDEX ON sockets.info(server_id, port);
COMMIT;


--sockets alarms indexes

----ON alarm_type

CREATE INDEX alarm_type_idx IF NOT EXISTS ON sockets.alarm USING GIN (to_tsvector('english', alarm_type));
COMMIT;
EXPLAIN SELECT * FROM sockets.alarm
    WHERE to_tsvector('english', alarm_type) @@ to_tsquery('english', 'warning');
	                                         QUERY PLAN                                         
--------------------------------------------------------------------------------------------
 Bitmap Heap Scan on alarm  (cost=2.53..6.61 rows=3 width=57)
   Recheck Cond: (to_tsvector('english'::regconfig, alarm_type) @@ '''warn'''::tsquery)
   ->  Bitmap Index Scan on alarm_type_idx  (cost=0.00..2.53 rows=3 width=0)
         Index Cond: (to_tsvector('english'::regconfig, alarm_type) @@ '''warn'''::tsquery)




