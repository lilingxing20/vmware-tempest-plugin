#!/usr/bin/env python
# coding=utf-8

'''
Author      : lixx (https://github.com/lilingxing20)
Created Time: Thu 01 Sep 2016 06:47:50 PM CST
File Name   : test_flavors.py
Description : 
'''
import uuid

from tempest.common.utils import data_utils
from tempest.lib import exceptions as lib_exc
from tempest import test

from vmware_tempest_plugin.tests.api.compute import base

class FlavorsAdminTestJSON(base.VmwareBaseV2ComputeTest):
    @classmethod
    def skip_checks(cls):
        super(FlavorsAdminTestJSON, cls).skip_checks()
        if not test.is_extension_enabled('OS-FLV-EXT-DATA', 'compute'):
            msg = "OS-FLV-EXT-DATA extension not enabled."
            raise cls.skipException(msg)

    @classmethod
    def setup_clients(cls):
        super(FlavorsAdminTestJSON, cls).setup_clients()
        cls.client = cls.os_adm.flavors_client
        cls.user_client = cls.os.flavors_client

    @classmethod
    def resource_setup(cls):
        super(FlavorsAdminTestJSON, cls).resource_setup()

        cls.flavor_name_prefix = 'test_flavor_'
        cls.ram = 512
        cls.vcpus = 1
        cls.disk = 10
        cls.ephemeral = 10
        cls.swap = 1024
        cls.rxtx = 2

    def flavor_clean_up(self, flavor_id):
        self.client.delete_flavor(flavor_id)
        self.client.wait_for_resource_deletion(flavor_id)

    def _create_flavor(self, flavor_id):
        # Create a flavor and ensure it is listed
        # This operation requires the user to have 'admin' role
        flavor_name = data_utils.rand_name(self.flavor_name_prefix)

        # Create the flavor
        flavor = self.client.create_flavor(name=flavor_name,
                                           ram=self.ram, vcpus=self.vcpus,
                                           disk=self.disk,
                                           id=flavor_id,
                                           ephemeral=self.ephemeral,
                                           swap=self.swap,
                                           rxtx_factor=self.rxtx)['flavor']
        self.addCleanup(self.flavor_clean_up, flavor['id'])
        self.assertEqual(flavor['name'], flavor_name)
        self.assertEqual(flavor['vcpus'], self.vcpus)
        self.assertEqual(flavor['disk'], self.disk)
        self.assertEqual(flavor['ram'], self.ram)
        self.assertEqual(flavor['swap'], self.swap)
        self.assertEqual(flavor['rxtx_factor'], self.rxtx)
        self.assertEqual(flavor['OS-FLV-EXT-DATA:ephemeral'],
                         self.ephemeral)
        self.assertEqual(flavor['os-flavor-access:is_public'], True)

        # Verify flavor is retrieved
        flavor = self.client.show_flavor(flavor['id'])['flavor']
        self.assertEqual(flavor['name'], flavor_name)

        return flavor['id']

    @test.idempotent_id('8b4330e1-12c4-4554-9390-e6639971f086')
    def test_create_flavor_with_int_id(self):
        flavor_id = data_utils.rand_int_id(start=1000)
        new_flavor_id = self._create_flavor(flavor_id)
        self.assertEqual(new_flavor_id, str(flavor_id))

    @test.idempotent_id('94c9bb4e-2c2a-4f3c-bb1f-5f0daf918e6d')
    def test_create_flavor_with_uuid_id(self):
        flavor_id = data_utils.rand_uuid()
        new_flavor_id = self._create_flavor(flavor_id)
        self.assertEqual(new_flavor_id, flavor_id)

    @test.idempotent_id('f83fe669-6758-448a-a85e-32d351f36fe0')
    def test_create_flavor_with_none_id(self):
        # If nova receives a request with None as flavor_id,
        # nova generates flavor_id of uuid.
        flavor_id = None
        new_flavor_id = self._create_flavor(flavor_id)
        self.assertEqual(new_flavor_id, str(uuid.UUID(new_flavor_id)))

