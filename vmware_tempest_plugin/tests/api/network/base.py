#!/usr/bin/env python
# coding=utf-8

'''
Author      : lixx (https://github.com/lilingxing20)
Created Time: Wed 31 Aug 2016 05:07:33 PM CST
File Name   : base.py
Description : 
'''

from tempest import config
from tempest.api.network import base


CONF = config.CONF


class VmwareBaseNetworkTest(base.BaseNetworkTest):
 
    force_tenant_isolation = False
    credentials = ['admin']
    _ip_version = 4
   
    @classmethod
    def setUpClass(cls):
        cls.set_network_resources()
        super(VmwareBaseNetworkTest, cls).setUpClass()
     

    @classmethod
    def skip_checks(cls):
#        super(VmwareBaseNetworkTest, cls).skip_checks()
#        if not CONF.service_available.neutron:
#            raise cls.skipException("Neutron support is required")
        if cls._ip_version == 6 and not CONF.network_feature_enabled.ipv6:
            raise cls.skipException("IPv6 Tests are disabled.")

    @classmethod
    def setup_credentials(cls):
        cls.set_network_resources()
        super(VmwareBaseNetworkTest, cls).setup_credentials()

    @classmethod
    def setup_clients(cls):
        cls.networks_client = cls.os_adm.networks_client
        cls.subnets_client = cls.os_adm.subnets_client

