#!/usr/bin/env python
# coding=utf-8

'''
Author      : lixx (https://github.com/lilingxing20)
Created Time: Mon 29 Aug 2016 03:07:09 PM CST
File Name   : test_volumes_list.py
Description : 
'''

import operator

from vmware_tempest_plugin.tests.api.volume import base
from tempest.common import waiters


class VolumesListAdminV2TestJSON(base.BaseVolumeAdminVmwareTest):

    @classmethod
    def resource_setup(cls):
        super(VolumesListAdminV2TestJSON, cls).resource_setup()
        # Create 3 test volumes
        cls.volume_list = []
        for i in range(3):
            volume = cls.create_volume()
            # Fetch volume details
            volume_details = cls.volumes_client.show_volume(
                volume['id'])['volume']
            cls.volume_list.append(volume_details)

    def test_volume_list_param_tenant(self):
        # Test to list volumes from single tenant
        # Create a volume in admin tenant
        from nose.tools import set_trace;set_trace()
        #adm_vol = self.admin_volume_client.create_volume()['volume']
        adm_vol = self.create_volume()
        waiters.wait_for_volume_status(self.admin_volume_client,
                                       adm_vol['id'], 'available')
        #self.addCleanup(self.admin_volume_client.delete_volume, adm_vol['id'])
        self.admin_volume_client.delete_volume(adm_vol['id'])

        params = {'all_tenants': 1,
                  'project_id': self.volumes_client.tenant_id}
        # Getting volume list from primary tenant using admin credentials
        fetched_list = self.admin_volume_client.list_volumes(
            detail=True, params=params)['volumes']
        # Verifying fetched volume ids list is related to primary tenant
        fetched_list_ids = map(operator.itemgetter('id'), fetched_list)
        expected_list_ids = map(operator.itemgetter('id'), self.volume_list)
        from nose.tools import set_trace;set_trace()
        self.assertEqual(sorted(expected_list_ids), sorted(fetched_list_ids))

        # Verifying tenant id of volumes fetched list is related to
        # primary tenant
        fetched_tenant_id = [operator.itemgetter(
            'os-vol-tenant-attr:tenant_id')(item) for item in fetched_list]
        expected_tenant_id = [self.volumes_client.tenant_id] * 3
        self.assertEqual(expected_tenant_id, fetched_tenant_id)

