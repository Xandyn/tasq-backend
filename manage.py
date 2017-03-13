# Stdlib imports
import random

# Core Flask imports

# Third-party app imports
from faker import Faker
from werkzeug.security import generate_password_hash

# Imports from your apps
from init.database import db
from application import application, init, manager


application.config.from_envvar('TASQ_SETTINGS')
db.init_app(application)
init()


@manager.command
def generate_fake():
    """
        generate fake users with projects & tasks
    """
    with application.app_context():
        from apps.users.models import User
        from apps.projects.models import Project
        from apps.tasks.models import Task

        fake = Faker()

        users = []
        for _ in range(5):
            user = User(
                name=fake.name(),
                email=fake.email(),
                password=generate_password_hash('123456')
            )
            db.session.add(user)
            db.session.flush()

            users.append(user)

        # save users
        db.session.commit()

        projects = []
        for user in users:
            for _ in range(random.randint(3, 5)):
                is_shared = fake.boolean(chance_of_getting_true=60)
                project = Project(
                    owner_id=user.id,
                    is_shared=is_shared,
                    name=fake.word()
                )
                db.session.add(project)
                db.session.flush()

                if is_shared:
                    rand_count = random.randint(1, 2)
                    rand_collabs = random.sample(users, k=rand_count)
                    while user.id in [x.id for x in rand_collabs]:
                        rand_collabs = random.sample(users, k=rand_count)

                    for collab in rand_collabs:
                        project.collaborators.append(collab)
                        db.session.add(project)
                        db.session.flush()

                projects.append(project)

        # save projects
        db.session.commit()

        for project in projects:
            tasks = []
            all_collabs = [x for x in project.collaborators.all()]
            all_collabs.append(project.owner)
            for _ in range(random.randint(4, 6)):
                creator = random.choice(all_collabs)
                notify_date = fake.date_time_this_month(before_now=False, after_now=True)
                task = Task(
                    creator_id=creator.id,
                    project_id=project.id,
                    text=' '.join(fake.words(nb=random.randint(1, 2))),
                    note=fake.sentence(),
                    notification_date=notify_date,
                    completion_date=notify_date
                )

                if project.is_shared:
                    is_assigned = fake.boolean(chance_of_getting_true=70)
                    if is_assigned:
                        assigned_to_user = random.choice(all_collabs)
                        task.assigned_to_user_id = assigned_to_user.id

                db.session.add(task)
                db.session.flush()
                tasks.append(task)

            for _ in range(random.randint(1, 2)):
                task = random.choice(tasks)
                task.is_completed = True
                task.completed_at = task.completion_date
                task.completed_by_user_id = task.assigned_to_user_id or task.creator_id

                db.session.add(task)
                db.session.flush()

            project.tasks_order = list([x.id for x in tasks])
            db.session.add(project)
            db.session.flush()

        # save tasks
        db.session.commit()


@manager.command
def del_all():
    """
        drop all tables
    """
    with application.app_context():
        from apps.users.models import User, Invite
        from apps.projects.models import Project, Collaborators
        from apps.tasks.models import Task

        Task.query.delete()
        Invite.query.delete()
        Collaborators.query.delete()
        Project.query.delete()
        User.query.delete()
        db.session.commit()


if __name__ == '__main__':
    with application.app_context():
        manager.run()
