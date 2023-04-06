#!/usr/bin/python3
"""
Fabric script that generates a tgz archive from the contents of the web_static
folder of the AirBnB Clone repo
"""

from datetime import datetime
from fabric.api import local


def do_pack():
    """
    Creates a .tgz archive
    """
    dtime = datetime.now().strftime('%Y%m%d%H%M%S')
    path = "versions/web_static_{}.tgz".format(dtime)
    local("mkdir  versions")

    if local("tar -cvzf {} web_static".format(path)).succeeded:
        return path
  
