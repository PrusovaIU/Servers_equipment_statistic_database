--tasks update indexes

CREATE INDEX IF NOT EXISTS tasks_updates_server_id_idx ON tasks.update_info(server_id);
COMMIT;
EXPLAIN SELECT updates.server_id, MAX(updates.time), servers.info.host
    FROM tasks.update_info as updates
    INNER JOIN servers.info ON updates.server_id = servers.info.server_id
    GROUP BY updates.server_id, servers.info.host
    ORDER BY updates.server_id;
                                       QUERY PLAN                                       
----------------------------------------------------------------------------------------
 GroupAggregate  (cost=46.33..51.67 rows=267 width=60)
   Group Key: updates.server_id, info.host
   ->  Sort  (cost=46.33..47.00 rows=267 width=60)
         Sort Key: updates.server_id, info.host
         ->  Hash Join  (cost=26.20..35.57 rows=267 width=60)
               Hash Cond: (updates.server_id = info.server_id)
               ->  Seq Scan on update_info updates  (cost=0.00..8.67 rows=267 width=12)
               ->  Hash  (cost=17.20..17.20 rows=720 width=52)
                     ->  Seq Scan on info  (cost=0.00..17.20 rows=720 width=52)



--modules info indexes

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

CREATE INDEX IF NOT EXISTS modules_info_type_idx ON modules.info(module_type);
COMMIT;
EXPLAIN SELECT server_id, ARRAY_AGG(module_id), ARRAY_AGG(position) FROM modules.info 
    WHERE module_type='A'
    GROUP BY server_id
    ORDER BY server_id;
                                           QUERY PLAN                                            
-------------------------------------------------------------------------------------------------
 Sort  (cost=5.29..5.32 rows=12 width=68)
   Sort Key: server_id
   ->  HashAggregate  (cost=4.90..5.08 rows=12 width=68)
         Group Key: server_id
         ->  Bitmap Heap Scan on info  (cost=1.82..4.49 rows=54 width=12)
               Recheck Cond: (module_type = 'A'::text)
               ->  Bitmap Index Scan on modules_info_type_idx  (cost=0.00..1.80 rows=54 width=0)
                     Index Cond: (module_type = 'A'::text)


--sockets info indexes

CREATE INDEX IF NOT EXISTS socket_info_server_id_idx ON sockets.info(server_id);
COMMIT;
EXPLAIN SELECT sockets.socket_id, servers_info.host, sockets.port, sockets.socket_type 
    FROM sockets.info AS sockets
    INNER JOIN servers.info AS servers_info ON sockets.server_id = servers_info.server_id
    WHERE sockets.server_id > 3 AND sockets.server_id < 10;
                                        QUERY PLAN                                        
------------------------------------------------------------------------------------------
 Nested Loop  (cost=0.15..25.45 rows=48 width=61)
   ->  Seq Scan on info sockets  (cost=0.00..2.41 rows=48 width=17)
         Filter: ((server_id > 3) AND (server_id < 10))
   ->  Index Scan using info_pkey on info servers_info  (cost=0.15..0.48 rows=1 width=52)
         Index Cond: (server_id = sockets.server_id)


CREATE INDEX IF NOT EXISTS socket_info_type_idx ON sockets.info(socket_type);
COMMIT;
EXPLAIN SELECT sockets.server_id, servers_info.host, ARRAY_AGG(sockets.socket_id), ARRAY_AGG(sockets.port)
    FROM sockets.info AS sockets
    INNER JOIN servers.info AS servers_info ON sockets.server_id = servers_info.server_id
    WHERE sockets.socket_type = 'net2'
    GROUP BY sockets.server_id, servers_info.host
    ORDER BY sockets.server_id;
                                              QUERY PLAN                                              
------------------------------------------------------------------------------------------------------
 GroupAggregate  (cost=21.16..21.73 rows=21 width=116)
   Group Key: sockets.server_id, servers_info.host
   ->  Sort  (cost=21.16..21.21 rows=21 width=60)
         Sort Key: sockets.server_id, servers_info.host
         ->  Nested Loop  (cost=0.15..20.69 rows=21 width=60)
               ->  Seq Scan on info sockets  (cost=0.00..2.17 rows=21 width=12)
                     Filter: (socket_type = 'net2'::text)
               ->  Index Scan using info_pkey on info servers_info  (cost=0.15..0.88 rows=1 width=52)
                     Index Cond: (server_id = sockets.server_id)

--sockets alarms indexes

CREATE INDEX IF NOT EXISTS socket_alarms_type_idx ON sockets.alarm(alarm_type);
COMMIT;
explain SELECT servers_info.server_id, servers_info.host, result.amount
    FROM servers.info AS servers_info
    INNER JOIN (
        SELECT sockets.server_id AS server_id, count(*) as amount FROM sockets.alarm AS alarms
            INNER JOIN sockets.info AS sockets ON sockets.socket_id = alarms.socket_id
            WHERE alarms.alarm_type = 'Error'
            GROUP BY server_id
    ) AS result
    ON servers_info.server_id = result.server_id;
                                        QUERY PLAN                                        
------------------------------------------------------------------------------------------
 Nested Loop  (cost=50.82..65.42 rows=12 width=60)
   ->  HashAggregate  (cost=50.67..50.79 rows=12 width=16)
         Group Key: sockets.server_id
         ->  Hash Join  (cost=3.12..46.15 rows=904 width=4)
               Hash Cond: (alarms.socket_id = sockets.socket_id)
               ->  Seq Scan on alarm alarms  (cost=0.00..40.55 rows=904 width=4)
                     Filter: (alarm_type = 'Error'::text)
               ->  Hash  (cost=1.94..1.94 rows=94 width=8)
                     ->  Seq Scan on info sockets  (cost=0.00..1.94 rows=94 width=8)
   ->  Index Scan using info_pkey on info servers_info  (cost=0.15..1.21 rows=1 width=52)
         Index Cond: (server_id = sockets.server_id)


