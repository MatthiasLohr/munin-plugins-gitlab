
# GitLab Plugins for Munin #

This is a collection of plugins for monitoring your GitLab instance with Munin.


## Setup ##

1. Clone this repository to your GitLab server. Create a new file called ```gitlab``` in ```/etc/munin/plugin-conf.d```
and copy+paste the following lines:
```
[gitlab_*]
user git
```
2. Change your directory to ```/etc/munin/plugins```. Create symlinks for each plugin (```ln -s```) which you want to
activate. Please take a look at the plugin specific documentation.


## Plugins ##

### gitlab_total_repo_count ###

Shows a global count of repositories, divided into code and wiki repositories.

No custom configuration.


### gitlab_total_repo_size ###

Shows the size of all your repositories, divided into code and wiki repositories.

No custom configuration.


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
