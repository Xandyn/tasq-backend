# Stdlib imports

# Core Flask imports
from flask import jsonify, request
from flask.views import MethodView

# Third-party app imports
from flask_jwt import jwt_required, current_identity
from sqlalchemy import or_
from sqlalchemy.orm.exc import NoResultFound

# Imports from your apps
from init.database import db
from init.utils import parse_json_to_object

from apps.tasks.models import Task
from apps.tasks.schemas import (
    TaskSchema, TaskCreateSchema
)


__all__ = (
    'TaskView',
)


class TaskView(MethodView):
    @jwt_required()
    def get(self):
        return jsonify({})

    @jwt_required()
    def post(self):
        json_data = request.get_json()
        result = TaskCreateSchema().load(json_data)

        if result.errors:
            return jsonify(result.errors), 403

        task = Task()
        parse_json_to_object(task, result.data)
        task.creator = current_identity

        db.session.add(task)
        db.session.flush()

        project = task.project
        tasks_order = list(project.tasks_order)
        tasks_order.insert(0, task.id)
        parse_json_to_object(project, {'tasks_order': tasks_order})

        db.session.add(project)
        db.session.commit()

        data = TaskSchema().dump(task).data
        return jsonify(data)

    @jwt_required()
    def put(self, item_id):
        return jsonify({})

    @jwt_required()
    def delete(self, item_id):
        return jsonify({})
