
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
