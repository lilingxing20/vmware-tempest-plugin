#!/usr/bin/env python
# coding=utf-8

'''
Author      : lixx (https://github.com/lilingxing20)
Created Time: Fri 26 Aug 2016 11:42:09 AM CST
File Name   : clients.py
Description : 
'''

from tempest import clients
from tempest import config
from vmware_tempest_plugin.services import volume

CONF = config.CONF


class ManagerVmware(clients.Manager):

    def __init__(self, credentials, service=None):
        super(ManagerVmware, self).__init__(credentials, service)
        self._set_volume_vmware_clients()

    def _set_volume_vmware_clients(self):
        params = self.parameters['volume']
        self.volumes_vmware_client = volume.v1.VmwareVolumesClient(
                self.auth_provider,
                default_volume_size=CONF.volume.volume_size,
                default_volume_type=CONF.volume_vmware.volume_type,
                **params)
        self.volumes_v2_vmware_client = volume.v2.VmwareVolumesClient(
                self.auth_provider,
                default_volume_size=CONF.volume.volume_size,
                default_volume_type=CONF.volume_vmware.volume_type,
                **params)
