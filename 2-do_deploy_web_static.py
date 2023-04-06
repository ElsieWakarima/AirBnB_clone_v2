#!/usr/bin/python3
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

    # upload archive to tmp directory of web server
    put(archive_path, '/tmp/')

    # extract archive to /data/web_static/releases/<archive filename without extension>
    filename = os.path.basename(archive_path)
    foldername = filename.split('.')[0]
    run('sudo mkdir -p /data/web_static/releases/{}/'.format(foldername))
    run('sudo tar -xzf /tmp/{} -C /data/web_static/releases/{}/'.format(filename, foldername))

    # delete archive from web server
    run('sudo rm /tmp/{}'.format(filename))

    # move contents of foldername to parent directory
    run('sudo mv /data/web_static/releases/{}/web_static/* /data/web_static/releases/{}/'.format(foldername, foldername))
    run('sudo rm -rf /data/web_static/releases/{}/web_static'.format(foldername))

    # delete symbolic link /data/web_static/current from web server
    run('sudo rm -rf /data/web_static/current')

    # create new symbolic link
    run('sudo ln -s /data/web_static/releases/{}/ /data/web_static/current'.format(foldername))

    return True
