#!/usr/bin/env python
# coding=utf-8

'''
Author      : lixx (https://github.com/lilingxing20)
Created Time: Fri 02 Sep 2016 04:13:05 PM CST
File Name   : test_servers.py
Description : 
'''

from tempest.common import compute
from tempest.common import fixed_network
from tempest.common.utils import data_utils
from tempest.common import waiters
from tempest.lib import decorators
from tempest import test

from vmware_tempest_plugin.tests.api.compute import base


class ServersAdminTestJSON(base.VmwareBaseV2ComputeTest):

    _host_key = 'OS-EXT-SRV-ATTR:host'

    @classmethod
    def setup_clients(cls):
        super(ServersAdminTestJSON, cls).setup_clients()
        cls.client = cls.os_adm.servers_client
        cls.non_admin_client = cls.servers_client
        cls.flavors_client = cls.os_adm.flavors_client

    @classmethod
    def resource_setup(cls):
        super(ServersAdminTestJSON, cls).resource_setup()

        cls.s1_name = data_utils.rand_name(cls.__name__ + '-server')
        server = cls.create_test_server(name=cls.s1_name,
                                        wait_until='ACTIVE')
        cls.s1_id = server['id']

        cls.s2_name = data_utils.rand_name(cls.__name__ + '-server')
        server = cls.create_test_server(name=cls.s2_name,
                                        wait_until='ACTIVE')
        cls.s2_id = server['id']

    @test.idempotent_id('51717b38-bdc1-458b-b636-1cf82d99f62f')
    def test_list_servers_by_admin(self):
        # Listing servers by admin user returns empty list by default
        body = self.client.list_servers(detail=True)
        servers = body['servers']
        self.assertEqual([], servers)

    @test.idempotent_id('9f5579ae-19b4-4985-a091-2a5d56106580')
    def test_list_servers_by_admin_with_all_tenants(self):
        # Listing servers by admin user with all tenants parameter
        # Here should be listed all servers
        params = {'all_tenants': ''}
        body = self.client.list_servers(detail=True, **params)
        servers = body['servers']
        servers_name = [server['name'] for server in servers]

        self.assertIn(self.s1_name, servers_name)
        self.assertIn(self.s2_name, servers_name)

#from nose.tools import set_trace;set_trace()
