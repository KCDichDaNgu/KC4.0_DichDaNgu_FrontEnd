from datetime import datetime
from abc import ABC, abstractmethod
from uuid import uuid4
from cassandra.cqlengine.models import Model
from cassandra.cqlengine import columns


class EntityBase(ABC, Model):

    id: columns.UUID(primary_key=True, default=uuid4)
    createdAt: columns.datetime
    updatedAt: columns.datetime
    