import uuid
from core.base_classes.entity import Entity
from cassandra.cqlengine import CQLEngineException, columns
from cassandra.cqlengine.models import Model


class TaskResult(Entity):
    task_id = columns.UUID(primary_key=True, default=uuid.uuid4)
    step = columns.Integer()
    result_url = columns.Text()

    class Meta:
        table_name = 'task_results'


class Task(Entity):
    id = columns.UUID(primary_key=True, default=uuid.uuid4)
    type = columns.Text(required=True)
    creator_type = columns.Text(required=True)
    status = columns.Text()
    current_step = columns.Integer()
    expired_date = columns.Date()
    task_result = TaskResult()

    class Meta:
        table_name = 'tasks'
