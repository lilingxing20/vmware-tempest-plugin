#!/usr/bin/env python
# coding=utf-8

'''
Author      : lixx (https://github.com/lilingxing20)
Created Time: Wed 31 Aug 2016 04:32:03 PM CST
File Name   : test_volume_hosts.py
Description : 
'''

from vmware_tempest_plugin.tests.api.volume import base
from tempest import test


class VolumeHostsAdminV2TestsJSON(base.BaseVolumeAdminVmwareTest):

    @test.idempotent_id('d5f3efa2-6684-4190-9ced-1c2f526352ad')
    def test_list_hosts(self):
        hosts = self.admin_hosts_client.list_hosts()['hosts']
        self.assertTrue(len(hosts) >= 2, "No. of hosts are < 2,"
                        "response of list hosts is: % s" % hosts)


#class VolumeHostsAdminV1TestsJSON(VolumeHostsAdminV2TestsJSON):
#    _api_version = 1
