
import os


class GitLabInstance(object):

    def __init__(self, gitlab_dir='/var/opt/gitlab'):
        self.gitlab_dir = gitlab_dir

    def get_data_dir(self):
        return os.path.join(self.gitlab_dir, 'git-data')

    def get_repository_dir(self):
        return os.path.join(self.get_data_dir(), 'repositories')

    def get_postgresql_dir(self):
        return os.path.join(self.gitlab_dir, 'postgresql')

    def get_db_connection(self):
        db_engine = os.environ.get('db_engine')
        if db_engine == None:
            db_engine = 'postgresql'
        dsn = os.environ.get('db_dsn')
        if dsn == None:
            dsn = 'host=' + self.get_postgresql_dir() + ' user=gitlab dbname=gitlabhq_production'
        if db_engine == 'postgresql':
            import psycopg2
            connection = psycopg2.connect(dsn)
        elif db_engine == 'mysql':
            import MySQLdb
            connection = MySQLdb.connect(dsn)
        return connection


def get_gitlab_instance():
    dir_variable = os.environ.get('gitlab_dir')
    if dir_variable:
        return GitLabInstance(dir_variable)
    else:
        return GitLabInstance()
