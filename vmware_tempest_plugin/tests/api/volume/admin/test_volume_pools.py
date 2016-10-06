#!/usr/bin/env python
# coding=utf-8

'''
Author      : lixx (https://github.com/lilingxing20)
Created Time: Wed 31 Aug 2016 04:19:11 PM CST
File Name   : test_volume_pools.py
Description : 
'''

from vmware_tempest_plugin.tests.api.volume import base
from tempest import test


class VolumePoolsAdminV2TestsJSON(base.VmwareBaseVolumeAdminTest):

    @classmethod
    def resource_setup(cls):
        super(VolumePoolsAdminV2TestsJSON, cls).resource_setup()
        # Create a test shared volume for tests
        cls.volume = cls.create_volume()

    @test.idempotent_id('0248a46c-e226-4933-be10-ad6fca8227e7')
    def test_get_pools_without_details(self):
        volume_info = self.admin_volume_vmware_client. \
            show_volume(self.volume['id'])['volume']
        cinder_pools = self.admin_volume_vmware_client.show_pools()['pools']
        self.assertIn(volume_info['os-vol-host-attr:host'],
                      [pool['name'] for pool in cinder_pools])

    @test.idempotent_id('d4bb61f7-762d-4437-b8a4-5785759a0ced')
    def test_get_pools_with_details(self):
        #from nose.tools import set_trace;set_trace()
        volume_info = self.admin_volume_vmware_client. \
            show_volume(self.volume['id'])['volume']
        cinder_pools = self.admin_volume_vmware_client.\
            show_pools(detail=True)['pools']
        self.assertIn(volume_info['os-vol-host-attr:host'],
                      [pool['name'] for pool in cinder_pools])

