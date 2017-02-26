# Stdlib imports

# Core Flask imports
from flask import Blueprint
# Third-party app imports

# Imports from your apps
from apps.projects.views import *


projects = Blueprint('projects', __name__, url_prefix='/projects')
projects_view = ProjectView.as_view('projects_view')


projects.add_url_rule(
    '',
    view_func=projects_view,
    methods=['GET', 'POST']
)

projects.add_url_rule(
    '/<int:item_id>',
    view_func=projects_view,
    methods=['PUT', 'DELETE']
)

collaborators = Blueprint('collaborators', __name__, url_prefix='/projects/collaborators')
collaborators_view = CollaboratorView.as_view('collaborators_view')


collaborators.add_url_rule(
    '',
    view_func=collaborators_view,
    methods=['DELETE']
)
