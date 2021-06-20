from conf import settings

from . import (
    mongo,
    filesystem
)


if settings['DB_DRIVER'] == 'mongodb':
    connection = mongo.RepoHost(**settings['DB_OPTS'])
elif settings['DB_DRIVER'] == 'filesystem':
    connection = filesystem.RepoHost(**settings['DB_OPTS'])
else:
    raise NotImplemented('DB Driver not found')


def get_connection():
    return connection
