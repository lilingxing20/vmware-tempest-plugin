#!/usr/bin/env python
# coding=utf-8

'''
Author      : lixx (https://github.com/lilingxing20)
Created Time: Fri 26 Aug 2016 11:42:09 AM CST
File Name   : clients.py
Description : 
'''

from oslo_log import log as logging
from tempest import config
from tempest import exceptions
from tempest import clients
from vmware_tempest_plugin.services import volume
 
CONF = config.CONF
LOG = logging.getLogger(__name__)
 
 
#class ManagerVmware(clients.Manager):
# 
#    def __init__(self, credentials, service=None, scope='project'):
#        super(ManagerVmware, self).__init__(credentials, service, scope)
#        self._set_volume_clients()
#
#    def _set_volume_clients(self):
#        self.vmware_volume_client = volume.VolumesVmwareClient(
#                self.auth_provider,
#                default_volume_size=CONF.volume.volume_size,
#                default_volume_type=CONF.volume_vmware.volume_size,
#                **params)
        #self.volumes_client = volume.VolumesVmwareClient(
        #        self.auth_provider,
        #        default_volume_size=CONF.volume.volume_size,
        #        default_volume_type=CONF.volume_vmware.volume_type,
        #        **params)

