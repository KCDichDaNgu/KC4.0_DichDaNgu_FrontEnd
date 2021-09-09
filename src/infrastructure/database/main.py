from infrastructure.configs import GlobalConfig
from cassandra.cqlengine import connection
from cassandra.auth import PlainTextAuthProvider

from infrastructure.configs.main import CassandraDatabase

def init_db(cassandraDbConfig: CassandraDatabase):

    auth_provider = PlainTextAuthProvider(
        username=cassandraDbConfig.USER, 
        password=cassandraDbConfig.PASSWORD
    )

    connection.setup(
        hosts=[cassandraDbConfig.HOST], 
        default_keyspace=cassandraDbConfig.KEYSPACE, 
        auth_provider=auth_provider,
        protocol_version=3
    )