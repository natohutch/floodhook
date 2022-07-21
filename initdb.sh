echo "local all postgres trust" > ./etc/postgresql/14/main/pg_hba.conf && echo "postgres configured"
service postgresql restart && echo "service started"
psql -U postgres -c "CREATE EXTENSION postgis; CREATE EXTENSION postgis_raster; CREATE EXTENSION postgres_fdw"
psql -U postgres -c "CREATE SERVER floodaware_server FOREIGN DATA WRAPPER postgres_fdw OPTIONS (host '${PG_SERVER_HOST}', dbname '${PG_SERVER_DB}', port '5432')"
psql -U postgres -c "CREATE USER MAPPING FOR postgres SERVER floodaware_server OPTIONS (user '${PG_SERVER_USER}', password '${PG_SERVER_PASS}')"
psql -U postgres -c "INSERT INTO spatial_ref_sys (srid, auth_name, auth_srid, proj4text) VALUES (100001, 'bom', 100001, '+proj=aea +lat_0=-34.2625 +lon_0=150.875 +lat_1=-32.7 +lat_2=-35.8 +x_0=0 +y_0=0 +ellps=GRS80 +units=km +no_defs')"
psql -U postgres -c "CREATE FOREIGN TABLE rainfall_raster (stamp timestamp without time zone, rast raster) SERVER floodaware_server"
exec $@