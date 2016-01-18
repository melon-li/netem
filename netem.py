#!/usr/bin/env python
#coding:utf-8

import sys
import re
from keystoneauth1.identity import v3
from keystoneauth1 import session
from novaclient import client
import community

AUTH_URL='http://192.168.99.112:35357/v3'
USERNAME='admin'
PASSWORD='bjtungirc'
PROJECT_NAME='demo'
USER_DOMAIN_ID='default'
PROJECT_DOMAIN_ID='default'

HOSTS_PATH='/etc/hosts'
MANIFESTS_PATH='/etc/puppet/manifests/site.pp'
IBR_CONFIG='/etc/puppet/files/ibrdtnd.conf'

def create_session():
    auth = v3.Password(auth_url=AUTH_URL, username=USERNAME,
                       password=PASSWORD, project_name=PROJECT_NAME,
                       user_domain_id=USER_DOMAIN_ID, project_domain_id=PROJECT_DOMAIN_ID)
    sess = session.Session(auth=auth)
    return sess

def update_etc_hosts(nova, hosts_path):
    '''update /etc/hosts,add the new experimental nodes,
    if an experimental node existed in hosts file, update it.
    '''

    #hosts_path = '/home/os/hh.txt'
    servers = nova.servers.list()
    with open(hosts_path, 'r') as hosts_obj:
        old_content = hosts_obj.read()

    with open(hosts_path, 'w') as hosts_obj:
        for server in servers:
            name = server.name
            addr = server.addresses['flat'][0]['addr']
            line = addr + ' ' + name
            if re.search(name+r'$', old_content):
                content = re.sub(r'.*'+name+r'$', line, old_content)
            else:
                content = old_content + '\n' + line

            old_content = content
        hosts_obj.write(content)


def create_manifests(model, MANIFESTS_PATH):
    '''creat puppet manifest, basing on mobility model,
    '''
    pass

def main():
    sess = create_session()
    nova = client.Client('2', session=sess)
    update_etc_hosts(nova, HOSTS_PATH)
    pass

if __name__ == "__main__":
    sys.exit(main())
