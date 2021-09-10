from datetime import datetime
from abc import ABC, abstractmethod
from uuid import uuid4
from cassandra.cqlengine.models import Model
from cassandra.cqlengine import columns


class OrmEntityBase(ABC, Model):

    id: columns.UUID(primary_key=True, default=uuid4)
    created_at: columns.datetime
    updated_at: columns.datetime
    