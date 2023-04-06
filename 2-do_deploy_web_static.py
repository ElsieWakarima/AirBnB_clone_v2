#!/usr/bin/env python3
"""
Distributes an archive to your web servers using Fabric
"""

from fabric.api import env, put, run, sudo
from os.path import exists
import os

env.hosts = ['54.174.248.63', '18.206.206.78']
env.user = 'ubuntu'  

def do_deploy(archive_path):
    """Deploys archive to web servers"""

    if not exists(archive_path):
        return False
        
    try:
        file_n = archive_path.split("/")[-1]
        no_ext = file_n.split(".")[0]
        path = "/data/web_static/releases/"
        put(archive_path, '/tmp/')
        run('mkdir -p {}{}/'.format(path, no_ext))
        run('tar -xzf /tmp/{} -C {}{}/'.format(file_n, path, no_ext))
        run('rm /tmp/{}'.format(file_n))
        run('mv {0}{1}/web_static/* {0}{1}/'.format(path, no_ext))
        run('rm -rf {}{}/web_static'.format(path, no_ext))
        run('rm -rf /data/web_static/current')
        run('ln -s {}{}/ /data/web_static/current'.format(path, no_ext))
        return True
    except:
        return False
