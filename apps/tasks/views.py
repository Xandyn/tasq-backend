# Stdlib imports
import datetime

# Core Flask imports
from flask import jsonify, request
from flask.views import MethodView

# Third-party app imports
from flask_jwt import jwt_required, current_identity
from sqlalchemy import or_

# Imports from your apps
from init.database import db
from init.utils import parse_json_to_object

from apps.users.models import User
from apps.projects.models import Project

from apps.tasks.models import Task
from apps.tasks.schemas import (
    TaskSchema, TaskCreateSchema
)


__all__ = (
    'TaskView',
)


class TaskView(MethodView):
    @jwt_required()
    def get(self, item_id=None):

        if item_id is None:

            project_ids = current_identity\
                .projects.with_entities(Project.id)
            invited_projects_ids = current_identity\
                .invited_projects.with_entities(Project.id)

            tasks = Task.query.filter(
                Task.is_deleted.is_(False)
            ).filter(or_(
                Task.project_id.in_(project_ids),
                Task.project_id.in_(invited_projects_ids),
            ))
            completed_tasks = tasks.filter(
                Task.is_completed.is_(True)
            )

            data = TaskSchema(many=True).dump(tasks).data
            return jsonify({
                'quantity': tasks.count(),
                'completed_quantity': completed_tasks.count(),
                'results': data
            })

        project = Project.query.get(item_id)
        if project is None:
            return jsonify({'error': 'Project not found.'}), 404

        if not self.is_project_member(project):
            return jsonify({'error': 'Project not found.'}), 404

        tasks = project.tasks
        completed_tasks = tasks.filter(
            Task.is_completed.is_(True)
        )

        data = TaskSchema(many=True).dump(tasks).data
        return jsonify({
            'quantity': tasks.count(),
            'completed_quantity': completed_tasks.count(),
            'results': data
        })

    @jwt_required()
    def post(self):
        json_data = request.get_json()
        result = TaskCreateSchema().load(json_data)

        if result.errors:
            return jsonify(result.errors), 403

        project = Project.query.get(result.data['project_id'])
        if project is None:
            return jsonify({'error': 'Project not found.'}), 404

        if not self.is_project_member(project):
            return jsonify({'error': 'Project not found.'}), 404

        task = Task()
        parse_json_to_object(task, result.data)
        task.creator = current_identity

        db.session.add(task)
        db.session.flush()

        tasks_order = list(project.tasks_order)
        tasks_order.insert(0, task.id)
        parse_json_to_object(project, {'tasks_order': tasks_order})

        db.session.add(project)
        db.session.commit()

        data = TaskSchema().dump(task).data
        return jsonify(data)

    @jwt_required()
    def put(self, item_id):
        json_data = request.get_json()
        task = Task.query.get(item_id)
        if task is None:
            return jsonify({'error': 'Task not found.'}), 404

        result = TaskSchema().load(json_data)

        if result.errors:
            return jsonify(result.errors), 403

        project = task.project
        if not self.is_project_member(project):
            return jsonify({'error': 'Project not found.'}), 404

        schema_data = result.data
        if schema_data.get('is_completed') is True:
            schema_data['completed_at'] = str(datetime.datetime.now())
            schema_data['completed_by_user_id'] = current_identity.id
        if schema_data.get('is_completed') is False:
            schema_data['completed_at'] = None
            schema_data['completed_by_user_id'] = None
        parse_json_to_object(task, result.data)

        db.session.add(task)
        db.session.commit()

        data = TaskSchema().dump(task).data
        return jsonify(data)

    @jwt_required()
    def delete(self, item_id):
        task = Task.query.get(item_id)
        if task is None:
            return jsonify({'error': 'Task not found.'}), 404

        project = task.project
        if not self.is_project_member(project):
            return jsonify({'error': 'Project not found.'}), 404

        task.is_deleted = True

        tasks_order = list(project.tasks_order)
        tasks_order.remove(task.id)
        parse_json_to_object(project, {'tasks_order': tasks_order})

        db.session.add(task)
        db.session.commit()

        return jsonify({})

    def is_project_member(self, project):
        is_member = False
        is_collaborator = project.collaborators.filter(
            User.id == current_identity.id
        ).first()
        if current_identity.id == project.owner_id or is_collaborator is not None:
            is_member = True
        return is_member
