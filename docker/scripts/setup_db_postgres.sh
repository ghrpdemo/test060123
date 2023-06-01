# !/bin/bash

HOSTPARAMS="-U postgres -h api-db -d postgres -p 26257 "
SQL="psql $HOSTPARAMS"
while true
    do
        rt=$($SQL --command "SELECT 1;")
        if [ $? -eq 0 ]; then
            echo "db is UP"
            break
        fi
         echo "db is not yet reachable, sleep for 1s before retry"
        sleep 1
    done

    echo "Creating api database ..."
    $SQL -c "CREATE DATABASE api;" \
        -c "CREATE USER api_user WITH PASSWORD '';" \
        -c "GRANT ALL PRIVILEGES ON DATABASE api TO api_user;" \
        -c "GRANT USAGE ON SCHEMA public TO api_user;" \
        -c "GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO api_user;" \
        -c "GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO api_user;" \
    echo "DB has been created"

$SQL -c "\connect api;" \
	-c "CREATE TABLE users(id SERIAL, name VARCHAR(50), PRIMARY KEY (id));" \
	-c "\copy users(id, name) FROM '/scripts/users.csv/users.csv' WITH CSV HEADER" \
        -c "SELECT setval(pg_get_serial_sequence('users', 'id'), coalesce(max(id)+1, 1), false) FROM users;"\
        -c "GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO api_user;" \
        -c "GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO api_user;" 
echo "CSV has been imported"
