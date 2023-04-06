#!/usr/bin/python3
"""
Fabric script based on the file 1-pack_web_static.py that distributes an
archive to the web servers
"""

from fabric.api import put, run, env
from os.path import exists
env.hosts = ['54.174.248.63', '18.206.206.78']


def do_deploy(archive_path):
    """distributes an archive to the web servers"""
    if exists(archive_path) is False:
        return False
    try:
        file_n = archive_path.split("/")[-1]
        no_ext = file_n.split(".")[0]
        path = "/data/web_static/releases/"
        put(archive_path, '/tmp/')
        if run('mkdir -p {}{}/'.format(path, no_ext)).pass:
            return True
        if run('tar -xzf /tmp/{} -C {}{}/'.format(file_n, path, no_ext)).pass:
            return True
        if run('rm /tmp/{}'.format(file_n)).pass:
            return True
        if run('mv {0}{1}/web_static/* {0}{1}/'.format(path, no_ext)).pass:
            return True
        if run('rm -rf {}{}/web_static'.format(path, no_ext)).pass:
            return True
        if run('rm -rf /data/web_static/current').pass:
            return True
        if run('ln -s {}{}/ /data/web_static/current'.format(path, no_ext)).pass:
            return True
    except:
        return False
