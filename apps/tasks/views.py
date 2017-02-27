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

        try:
            project = Project.query.get(item_id)
        except NoResultFound:
            return jsonify({
                'error': 'Project not found.'
            }), 404

        # TODO Repeat
        is_collaborator = project.collaborators.filter(
            User.id == current_identity.id
        ).first()
        if current_identity.id != project.owner_id and is_collaborator is None:
            return jsonify({
                'error': 'Project not found.'
            }), 404

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

        try:
            project = Project.query.get(result.data['project_id'])
        except NoResultFound:
            return jsonify({
                'error': 'Project not found.'
            }), 404

        # TODO Repeat
        is_collaborator = project.collaborators.filter(
            User.id == current_identity.id
        ).first()
        if current_identity.id != project.owner_id and is_collaborator is None:
            return jsonify({
                'error': 'Project not found.'
            }), 404

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
        try:
            task = Task.query.get(item_id)
        except NoResultFound:
            return jsonify({
                'error': 'Task not found.'
            }), 404

        result = TaskSchema().load(json_data)

        if result.errors:
            return jsonify(result.errors), 403

        # TODO Repeat
        project = task.project
        is_collaborator = project.collaborators.filter(
            User.id == current_identity.id
        ).first()
        if current_identity.id != project.owner_id and is_collaborator is None:
            return jsonify({
                'error': 'Project not found.'
            }), 404

        parse_json_to_object(task, result.data)

        db.session.add(task)
        db.session.commit()

        data = TaskSchema().dump(task).data
        return jsonify(data)

    @jwt_required()
    def delete(self, item_id):
        try:
            task = Task.query.get(item_id)
        except NoResultFound:
            return jsonify({
                'error': 'Task not found.'
            }), 404

        # TODO Repeat
        project = task.project
        is_collaborator = project.collaborators.filter(
            User.id == current_identity.id
        ).first()
        if current_identity.id != project.owner_id and is_collaborator is None:
            return jsonify({
                'error': 'Project not found.'
            }), 404

        task.is_deleted = True
        db.session.add(task)
        db.session.commit()

        return jsonify({})
