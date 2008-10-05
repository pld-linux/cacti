update poller_item set rrd_path= replace(rrd_path, '/usr/share/cacti/rra', '/var/lib/cacti/rra') where rrd_path like '/usr/share/cacti/rra/%';
