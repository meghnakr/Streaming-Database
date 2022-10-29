import os

from google.cloud.sql.connector import Connector, IPTypes
import pymysql

import sqlalchemy


# connect_with_connector initializes a connection pool for a
# Cloud SQL instance of MySQL using the Cloud SQL Python Connector.
def connect_with_connector() -> sqlalchemy.engine.base.Engine:

    instance_connection_name = 'cs348project-367000:us-central1:myhbodb'  # e.g. 'project:region:instance'
    db_user = 'root'  # e.g. 'my-db-user'
    db_pass = 'richard'  # e.g. 'my-db-password'
    db_name = 'streaming'  # e.g. 'my-database'

    ip_type = IPTypes.PRIVATE if os.environ.get("PRIVATE_IP") else IPTypes.PUBLIC

    connector = Connector(ip_type)

    def getconn() -> pymysql.connections.Connection:
        conn: pymysql.connections.Connection = connector.connect(
            instance_connection_name,
            "pymysql",
            user=db_user,
            password=db_pass,
            db=db_name,
        )
        return conn

    pool = sqlalchemy.create_engine(
        "mysql+pymysql://",
        creator=getconn,
        # ...
    )
    return pool

