#!/usr/bin/env python
# coding=utf-8

'''
Author      : lixx (https://github.com/lilingxing20)
Created Time: Mon 29 Aug 2016 03:17:05 PM CST
File Name   : base.py
Description : 
'''

from tempest.api.volume import base 
from tempest.common.utils import data_utils
from tempest.common import waiters
from tempest import config
from oslo_log import log as logging

from vmware_tempest_plugin.services import volume

CONF = config.CONF
LOG = logging.getLogger(__name__)

class BaseVolumeAdminVmwareTest(base.BaseVolumeAdminTest):
    @classmethod
    def setup_clients(cls):
        super(BaseVolumeAdminVmwareTest, cls).setup_clients()

    @classmethod
    def create_volume(cls, **kwargs):
        """Wrapper utility that returns a test volume."""
        name = data_utils.rand_name(cls.__name__ + '-Volume')

        name_field = cls.special_fields['name_field']
        kwargs[name_field] = name
        kwargs['volume_type'] = CONF.volume_vmware.volume_type
        LOG.info('Used volume type %s for create volume.' %  kwargs['volume_type'])

        volume = cls.volumes_client.create_volume(**kwargs)['volume']
        cls.volumes.append(volume)
        waiters.wait_for_volume_status(cls.volumes_client,
                                       volume['id'], 'available')
        return volume

