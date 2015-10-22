
# GitLab Plugins for Munin #

This is a collection of plugins for monitoring your [GitLab](http://www.gitlab.com/) instance with
[Munin](http://munin-monitoring.org/).

These plugins are developed for and tested with GitLab versions >= 8.0.0.
Maybe some plugins may work with older GitLab instances, but there's no
support for occuring bugs or errors.


## Setup ##

1. Clone this repository to your GitLab server. Create a new file called ```gitlab``` in ```/etc/munin/plugin-conf.d```
and copy+paste the following lines:
```
[gitlab_*]
user git
#env.gitlab_dir /var/opt/gitlab    # optional, defaults to GitLab omnibus package setup directory

## using a PostgreSQL database
#env.db_engine postgresql          # optional, defaults to postgres, valid values: postgresql. mysql
#env.db_dsn host=/var/opt/gitlab/postgresql user=gitlab dbname=gitlabhq_production  # optional, defaults to GitLab omnibus database

## using a MySQL database
#env.db_engine mysql
#env.db_dsn host=localhost user=gitlab db=gitlabhq_production

[gitlab_redis_*]
user gitlab-redis
#env.redis_socket /var/opt/gitlab/redis/redis.socket  # optional, defaults to GitLab omnibus redis instance
```
2. Change your directory to ```/etc/munin/plugins```. Create symlinks for each plugin (```ln -s```) which you want to
activate. Please take a look at the plugin specific documentation.


## Plugins ##

### Plugin configuration ###

All plugins will use the default omnibus gitlab setup configuration. You can customize the behaviour with the following parameters:




## Further Monitoring ##

### bundled nginx ###

If you want to monitor the bundled nginx instance you have to enable the status module. Supposed you have no other
nginx instance running, create a file ```/etc/nginx/conf.d/status.conf``` and add the following lines:

```
server  {
    listen *:80;
    listen [::]:80;
    server_name localhost;
    location /nginx_status {
        stub_status on;
        access_log off;
        allow 127.0.0.1;
        allow ::1;
        deny all;
    }
}
```

In ```/etc/gitlab/gitlab.rb``` update your configuration:
```ruby
nginx['custom_nginx_config'] = "include /etc/nginx/conf.d/*.conf;"
```

After ```gitlab-ctl reconfigure``` and ```gitlab-ctl restart``` you should be able to use the default nginx plugins for
munin to monitor your gitlab nginx instance. You can activate them via:

```
ln -s /usr/share/munin/plugins/nginx_request /etc/munin/plugins
ln -s /usr/share/munin/plugins/nginx_status /etc/munin/plugins
/etc/init.d/munin-node restart
```
