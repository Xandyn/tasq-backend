from redis import Redis
from init.flask_init import application

redis = Redis(host=application.config['REDIS_HOST'], password=application.config['REDIS_PASSWORD'])
