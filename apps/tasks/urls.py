# Stdlib imports

# Core Flask imports
from flask import Blueprint

# Third-party app imports

# Imports from your apps
from apps.tasks.views import *


tasks = Blueprint('tasks', __name__, url_prefix='/tasks')
tasks_view = TaskView.as_view('tasks_view')


tasks.add_url_rule(
    '',
    view_func=tasks_view,
    methods=['GET', 'POST']
)

tasks.add_url_rule(
    '/<int:item_id>',
    view_func=tasks_view,
    methods=['GET', 'PUT', 'DELETE']
)
