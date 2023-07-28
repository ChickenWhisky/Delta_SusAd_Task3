FROM postgres:14

# Copy the SQL script to the container's initialization directory
COPY ./scripts/init.sql /docker-entrypoint-initdb.d/

EXPOSE 5432