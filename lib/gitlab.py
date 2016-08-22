
import os
import socket


class GitLabInstance(object):

    def __init__(self, gitlab_dir='/var/opt/gitlab'):
        self.gitlab_dir = gitlab_dir

    def get_data_dir(self):
        return os.path.join(self.gitlab_dir, 'git-data')

    @property
    def shared_dir(self):
        return os.path.join(self.gitlab_dir, 'gitlab-rails', 'shared')

    def get_artifacts_dir(self):
        return os.path.join(self.shared_dir, 'artifacts')

    def get_registry_dir(self):
        return os.path.join(self.shared_dir, 'registry')

    def get_repository_dir(self):
        return os.path.join(self.get_data_dir(), 'repositories')

    def get_postgresql_dir(self):
        return os.path.join(self.gitlab_dir, 'postgresql')

    def get_db_connection(self):
        db_engine = os.environ.get('db_engine')
        if db_engine is None:
            db_engine = 'postgresql'
        dsn = os.environ.get('db_dsn')
        if dsn is None:
            dsn = 'host=' + self.get_postgresql_dir() + ' user=gitlab dbname=gitlabhq_production'
        connection = None
        if db_engine == 'postgresql':
            import psycopg2
            connection = psycopg2.connect(dsn)
            search_path = os.environ.get('db_pg_search_path')
            if not search_path is None:
                cursor = connection.cursor()
                cursor.execute('SET search_path TO ' + search_path)
                cursor.close()
        elif db_engine == 'mysql':
            import MySQLdb
            import re
            cparams = dict(re.findall(r'(\S+)=(".*?"|\S+)', dsn))
            print(cparams)
            connection = MySQLdb.connect(**cparams)
        return connection

    def get_redis_connection(self):
        socket_name = os.environ.get('redis_socket')
        if socket_name is None:
            socket_name = '/var/opt/gitlab/redis/redis.socket'
        connection = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        try:
            connection.connect(socket_name)
        except socket.error:
            return None
        return connection

    def get_redis_info(self):
        redis = self.get_redis_connection()
        if redis is None:
            raise GitLabError('Redis connection not available')
        redis.send('INFO\r\n')
        data = redis.recv(16384)
        redis.close()
        info = {}
        for line in data.split('\n'):
            line = line.strip()
            if len(line) == 0:
                continue
            if line.startswith('$'):
                continue
            if line.startswith('#'):
                continue
            (key, value) = line.split(':', 2)
            info[key] = value
        return info

    def get_redis_config(self, param):
        redis = self.get_redis_connection()
        if redis is None:
            raise GitLabError('Redis connection not available')
        redis.send('*3\r\n$6\r\nCONFIG\r\n$3\r\nGET\r\n$' + str(len(param)) + '\r\n' + param + '\r\n')
        data = redis.recv(16384)
        redis.close()
        values = []
        for line in data.split('\n'):
            line = line.strip()
            if len(line) == 0:
                continue
            if line.startswith('*'):
                continue
            if line.startswith('$'):
                continue
            if line.startswith('#'):
                continue
            values.append(line)
        return values

    def get_redis_max_clients(self):
        config = self.get_redis_config('maxclients')
        return config[1]

    def get_redis_max_memory(self):
        config = self.get_redis_config('maxmemory')
        return config[1]


class GitLabError(Exception):

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


def get_gitlab_instance():
    dir_variable = os.environ.get('gitlab_dir')
    if dir_variable:
        return GitLabInstance(dir_variable)
    else:
        return GitLabInstance()

