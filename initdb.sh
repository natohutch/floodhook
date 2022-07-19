echo "local all postgres trust" > ./etc/postgresql/14/main/pg_hba.conf && echo "postgres configured"
service postgresql restart && echo "service started"
psql -U postgres -c "CREATE EXTENSION postgis; CREATE EXTENSION postgis_raster; CREATE EXTENSION postgres_fdw"
psql -U postgres -c "CREATE SERVER floodaware_server FOREIGN DATA WRAPPER postgres_fdw OPTIONS (host 'floodaware-db.postgres.database.azure.com', dbname 'floodaware', port '5432')"
psql -U postgres -c "CREATE USER MAPPING FOR postgres SERVER floodaware_server OPTIONS (user #####, password #####)"
psql -U postgres -c "CREATE FOREIGN TABLE raster_temp2 (rid integer, rast raster) SERVER floodaware_server"
exec $@