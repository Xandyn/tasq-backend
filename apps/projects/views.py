# -*- coding: utf-8 -*-

# Stdlib imports

# Core Flask imports
from flask import jsonify, request
from flask.views import MethodView

# Third-party app imports
from flask_jwt import jwt_required, current_identity
from sqlalchemy.orm.exc import NoResultFound

# Imports from your apps
from init.database import db
from init.utils import parse_json_to_object, generate_jwt_token

from apps.projects.models import Project
from apps.projects.schemas import ProjectSchema
from apps.users.models import Invite


__all__ = (
    'ProjectView',
)


class ProjectView(MethodView):
    @jwt_required()
    def get(self):
        query = Project.query.filter(
            Project.owner_id == current_identity.id,
        )
        projects = query.filter(
            Project.is_deleted.is_(False)
        )
        not_viewed_projects = query.filter(
            Project.is_deleted.is_(True)
        )

        quantity = projects.count()
        not_viewed_quantity = not_viewed_projects.count()

        data = ProjectSchema(many=True).dump(projects).data
        return jsonify({
            'quantity': quantity,
            'not_viewed_quantity': not_viewed_quantity,
            'results': data
        })

    def post(self):
        json_data = request.get_json()
        # collaborators = json_data.pop('collaborators', [])
        result = ProjectSchema().load(json_data)

        if result.errors:
            return jsonify(result.errors), 403

        project = Project()
        parse_json_to_object(project, result.data)

        db.session.add(project)

        # if collaborators:
        #     for collaborator in collaborators:
        #         inv = Invite()

        db.session.commit()

        data = ProjectSchema().dump(project).data
        return jsonify(data)

    @jwt_required()
    def put(self, item_id):
        json_data = request.get_json()
        try:
            project = Project.query.get(int(item_id))
        except NoResultFound:
            return jsonify({
                'message': 'Project not found.'
            }), 404

        result = ProjectSchema().load(json_data)

        if result.errors:
            return jsonify(result.errors), 403

        parse_json_to_object(project, result.data)

        db.session.add(project)
        db.session.commit()

        data = ProjectSchema().dump(project).data
        return jsonify(data)

    @jwt_required()
    def delete(self, item_id):
        try:
            project = Project.query.get(int(item_id))
        except NoResultFound:
            return jsonify({
                'message': 'Project not found.'
            }), 404

        project.is_deleted = True

        db.session.add(project)
        db.session.commit()

        return jsonify({
            'success': True
        })
