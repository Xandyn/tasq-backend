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
