
import os
import psycopg2


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
        connection = psycopg2.connect(host=self.get_postgresql_dir(), user='gitlab', database='gitlabhq_production')
        return connection


def get_gitlab_instance():
    dir_variable = os.environ.get('gitlab_dir')
    if dir_variable:
        return GitLabInstance(dir_variable)
    else:
        return GitLabInstance()
