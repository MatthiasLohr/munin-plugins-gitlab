
# GitLab Plugins for Munin #

This is a collection of plugins for monitoring your [GitLab](https://about.gitlab.com/) instance with
[Munin](https://munin-monitoring.org/).

These plugins are developed for and tested with GitLab versions >= 18.10.0.
Maybe some plugins may work with older GitLab instances, but there's no
support for occurring bugs or errors.


## Setup ##

1. Install dependencies depending on your distribution:
  * Ubuntu and Debian
    ```
    sudo apt-get install python-psycopg2
    ```
2. Clone this repository to your GitLab server. Create a new file called ```gitlab``` in ```/etc/munin/plugin-conf.d```
and copy+paste the following lines:
  ```
  [gitlab_*]
  user git
  #env.gitlab_dir /var/opt/gitlab    # optional, defaults to GitLab omnibus package setup directory

  ## using a PostgreSQL database
  #env.db_engine postgresql          # optional, defaults to postgres, valid values: postgresql. mysql
  #env.db_dsn host=/var/opt/gitlab/postgresql user=gitlab dbname=gitlabhq_production  # optional, defaults to GitLab omnibus database
  #env.db_pg_search_path gitlab     # optional, set search_path before executing any query. Useful if not using GitLab omnibus package

  ## using a MySQL database
  #env.db_engine mysql
  #env.db_dsn host=localhost user=gitlab db=gitlabhq_production

  [gitlab_redis_*]
  user gitlab-redis
  #env.redis_socket /var/opt/gitlab/redis/redis.socket  # optional, defaults to GitLab omnibus redis instance

  [gitlab_total_registry_size]
  user registry
  ```
3. Change your directory to ```/etc/munin/plugins```. Create symlinks for each plugin (```ln -s```) which you want to
activate. Please take a look at the plugin specific documentation.


## Plugins ##

### Plugin configuration ###

All plugins will use the default omnibus gitlab setup configuration on Debian and Ubuntu.

## Further Monitoring ##

### bundled nginx ###

If you want to monitor the bundled nginx instance you can use the already active nginx status module.
Check the file `/var/opt/gitlab/nginx/conf/nginx-status.conf` for details if defaults where changed.

In case the file is not there, check the `gitlab.rb` file for `nginx['status']` and enable it.
In ```/etc/gitlab/gitlab.rb``` update your configuration:
```ruby
nginx['status'] = {
    "enable" => true
}
```

After ```gitlab-ctl reconfigure``` and ```gitlab-ctl restart``` you should be able to use the default nginx plugins for
munin to monitor your gitlab nginx instance.
First create a file in ```/etc/munin/plugin-conf.d``` (change the port to your config):
```
[nginx_*]
  env.url http://localhost:8060/nginx_status
```
Next create the links for the Munin plugins and restart munin-node:
```
sudo ln -s /usr/share/munin/plugins/nginx_request /etc/munin/plugins
sudo ln -s /usr/share/munin/plugins/nginx_status /etc/munin/plugins
sudo systemctl restart munin-node
```

### bundled postgresql ###

Install the needed additional Debian packages:
```
sudo apt install libdbd-pg-perl
```
Create the config file in ```/etc/munin/plugin-conf.d``` (make sure it is alphabetically after ```munin-node```)
```
[postgres_*]
  user git
  env.PGHOST /var/opt/gitlab/postgresql
  env.PGUSER gitlab
  env.PGDATABASE gitlabhq_production
```
Afterwards links to the postgres munin plugins can be created. Here an example:
```
sudo ln -s /usr/share/munin/plugins/postgres_users /etc/munin/plugins
```
or by using the suggestion of munin to display possible links:
```
sudo munin-node-configure --suggest --shell
```
As usual restart munin-node after changes:
```
sudo systemctl restart munin-node
```

### bundled multips ###

It might be useful to view how many gitlab processes are running and how many memory they use.

Create the config file in ```/etc/munin/plugin-conf.d``` to specify the processes to monitor:
```
[multips_gitlab]
  env.names postgres puma sidekiq ruby
  env.regex_puma bundle
  env.regex_sidekiq \(bundle\|ruby\)

[multips_memory_gitlab]
  env.names postgres bundle ruby
```
Create links for the munin-plugins:
```
sudo ln -s /usr/share/munin/plugins/multips /etc/munin/plugins/multips_gitlab
sudo ln -s /usr/share/munin/plugins/multips_memory /etc/munin/plugins/multips_memory_gitlab
```
Restart munin-node:
```
sudo systemctl restart munin-node
```

