#!/usr/bin/env python
# coding=utf-8

'''
Author      : lixx (https://github.com/lilingxing20)
Created Time: Thu 01 Sep 2016 07:20:03 PM CST
File Name   : test_services.py
Description : 
'''

from tempest import config
from vmware_tempest_plugin.tests.api.compute import base

CONF = config.CONF


class ServicesAdminTestJSON(base.VmwareBaseV2ComputeTest):

    @classmethod
    def setup_clients(cls):
        super(ServicesAdminTestJSON, cls).setup_clients()
        cls.client = cls.os_adm.services_client

    def test_list_services(self):
        services = self.client.list_services()['services']
        self.assertNotEqual(0, len(services))

