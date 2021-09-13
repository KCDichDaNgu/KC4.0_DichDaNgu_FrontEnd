from infrastructure.configs import GlobalConfig
from cassandra.cqlengine import connection
from cassandra.auth import PlainTextAuthProvider
from cassandra.cqlengine.management import _create_keyspace
from infrastructure.configs.main import CassandraDatabase
from infrastructure.database.base_classes.aiocqlengine.session import aiosession_for_cqlengine

import asyncio

def init_db(cassandraDbConfig: CassandraDatabase):

    auth_provider = PlainTextAuthProvider(
        username=cassandraDbConfig.USER,
        password=cassandraDbConfig.PASSWORD
    )

    connection.setup(
        hosts=[cassandraDbConfig.HOST],
        default_keyspace=cassandraDbConfig.KEYSPACE.NAME,
        auth_provider=auth_provider,
        protocol_version=cassandraDbConfig.PROTOCOL_VERSION
    )
    
    _create_keyspace(
        name=cassandraDbConfig.KEYSPACE.NAME, 
        durable_writes=cassandraDbConfig.KEYSPACE.DURABLE_WRITES, 
        strategy_class=cassandraDbConfig.KEYSPACE.STRATEGY_CLASS,
        strategy_options=cassandraDbConfig.KEYSPACE.STRATEGY_OPTIONS, 
        connections=cassandraDbConfig.KEYSPACE.CONNECTIONS
    )

    current_session = connection.session

    current_session.set_keyspace(cassandraDbConfig.KEYSPACE.NAME)
    
    aiosession_for_cqlengine(current_session)
    
    connection.set_session(current_session)
