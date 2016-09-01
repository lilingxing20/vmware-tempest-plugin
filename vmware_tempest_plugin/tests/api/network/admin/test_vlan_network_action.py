#!/usr/bin/env python
# coding=utf-8

'''
Author      : lixx (https://github.com/lilingxing20)
Created Time: Wed 31 Aug 2016 05:20:39 PM CST
File Name   : test_vlan_network_action.py
Description : 
'''



import netaddr
import six
from vmware_tempest_plugin.tests.api.network import base
from tempest.common import custom_matchers
from tempest.common.utils import data_utils
from tempest import config


CONF = config.CONF


class DVSNetworksTest(base.VmwareBaseNetworkTest):

    @classmethod
    def resource_setup(cls):
        super(DVSNetworksTest, cls).resource_setup()
        cls.network = cls.create_network()
        cls.name = cls.network['name']
        cls.subnet = cls._create_subnet_with_last_subnet_block(cls.network,
                                                               cls._ip_version)
        cls._subnet_data = {6: {'gateway':
                                str(cls._get_gateway_from_tempest_conf(6)),
                                'allocation_pools':
                                cls._get_allocation_pools_from_gateway(6),
                                'dns_nameservers': ['2001:4860:4860::8844',
                                                    '2001:4860:4860::8888'],
                                'host_routes': [{'destination': '2001::/64',
                                                 'nexthop': '2003::1'}],
                                'new_host_routes': [{'destination':
                                                     '2001::/64',
                                                     'nexthop': '2005::1'}],
                                'new_dns_nameservers':
                                ['2001:4860:4860::7744',
                                 '2001:4860:4860::7888']},
                            4: {'gateway':
                                str(cls._get_gateway_from_tempest_conf(4)),
                                'allocation_pools':
                                cls._get_allocation_pools_from_gateway(4),
                                'dns_nameservers': ['8.8.4.4', '8.8.8.8'],
                                'host_routes': [{'destination': '10.20.0.0/32',
                                                 'nexthop': '10.100.1.1'}],
                                'new_host_routes': [{'destination':
                                                     '10.20.0.0/32',
                                                     'nexthop':
                                                     '10.100.1.2'}],
                                'new_dns_nameservers': ['7.8.8.8', '7.8.4.4']}}
#    @classmethod
#    def resource_cleanup(cls):
#        " do not delete network "
#        pass 

    def test_a_create_update_delete_network_subnet(self):
        " Create a network "
        name = data_utils.rand_name('network-')       
        network = self.create_network(network_name=name)
        self.addCleanup(self._delete_network, network)
        net_id = network['id']
        self.net_id = net_id
        self.assertEqual('ACTIVE', network['status'])
        "network update"
        new_name = data_utils.rand_name('new-network-')
        body = self.networks_client.update_network(net_id, name=new_name)
        updated_net = body['network']
        self.assertEqual(updated_net['name'], new_name)
        "Find a cidr that is not in use yet and create a subnet with it"
        subnet = self.create_subnet(network)
        subnet_id = subnet['id']
        "subnet update"
        new_name = "New_subnet"
        body = self.subnets_client.update_subnet(subnet_id, name=new_name)
        updated_subnet = body['subnet']
        self.assertEqual(updated_subnet['name'], new_name)
        
    def test_b_show_network(self):
        "show network"
        body = self.networks_client.show_network(self.network['id'])
        network = body['network']
        for key in ['id', 'name']:
            self.assertEqual(network[key], self.network[key])
            print network

    def test_c_show_network_fields(self):
        fields = ['id', 'name']
        body = self.networks_client.show_network(self.network['id'],
                                                 fields=fields)
        network = body['network']
        self.assertEqual(sorted(network.keys()), sorted(fields))
        for field_name in fields:
            self.assertEqual(network[field_name], self.network[field_name])
            print ">>>>", network

    def test_d_list_networks(self):
        body = self.networks_client.list_networks()
        networks = [network['id'] for network in body['networks']
                    if network['id'] == self.network['id']]
        self.assertNotEmpty(networks, "Created network not found in the list")
        
    def test_e_delete_network(self):
        "delete network"
        body = self.networks_client.delete_network(self.network['id'])
        self.assertEqual(204, body.response.status)

    @classmethod
    def _create_subnet_with_last_subnet_block(cls, network, ip_version):
        if ip_version == 4:
            cidr = netaddr.IPNetwork(CONF.network.project_network_cidr)
            mask_bits = CONF.network.project_network_mask_bits
        elif ip_version == 6:
            cidr = netaddr.IPNetwork(CONF.network.project_network_v6_cidr)
            mask_bits = CONF.network.project_network_v6_mask_bits

        subnet_cidr = list(cidr.subnet(mask_bits))[-1]
        gateway_ip = str(netaddr.IPAddress(subnet_cidr) + 1)
        return cls.create_subnet(network, gateway=gateway_ip,
                                 cidr=subnet_cidr, mask_bits=mask_bits)

    @classmethod
    def _get_gateway_from_tempest_conf(cls, ip_version):
        """Return first subnet gateway for configured CIDR """
        if ip_version == 4:
            cidr = netaddr.IPNetwork(CONF.network.project_network_cidr)
            mask_bits = CONF.network.project_network_mask_bits
        elif ip_version == 6:
            cidr = netaddr.IPNetwork(CONF.network.project_network_v6_cidr)
            mask_bits = CONF.network.project_network_v6_mask_bits

        if mask_bits >= cidr.prefixlen:
            return netaddr.IPAddress(cidr) + 1
        else:
            for subnet in cidr.subnet(mask_bits):
                return netaddr.IPAddress(subnet) + 1

    @classmethod
    def _get_allocation_pools_from_gateway(cls, ip_version):
        """Return allocation range for subnet of given gateway"""
        gateway = cls._get_gateway_from_tempest_conf(ip_version)
        return [{'start': str(gateway + 2), 'end': str(gateway + 3)}]

#    def subnet_dict(self, include_keys):
#        return dict((key, self._subnet_data[self._ip_version][key])
#                    for key in include_keys)
#
#    def _compare_resource_attrs(self, actual, expected):
#        exclude_keys = set(actual).symmetric_difference(expected)
#        self.assertThat(actual, custom_matchers.MatchesDictExceptForKeys(
#                        expected, exclude_keys))

    def _delete_network(self, network):
        self.networks_client.delete_network(network['id'])
        if network in self.networks:
            self.networks.remove(network)
        for subnet in self.subnets:
            if subnet['network_id'] == network['id']:
                self.subnets.remove(subnet)

#    def _create_verify_delete_subnet(self, cidr=None, mask_bits=None,
#                                     **kwargs):
#        network = self.create_network()
#        net_id = network['id']
#        gateway = kwargs.pop('gateway', None)
#        subnet = self.create_subnet(network, gateway, cidr, mask_bits,
#                                    **kwargs)
#        compare_args_full = dict(gateway_ip=gateway, cidr=cidr,
#                                 mask_bits=mask_bits, **kwargs)
#        compare_args = dict((k, v) for k, v in six.iteritems(compare_args_full)
#                            if v is not None)
#
#        if 'dns_nameservers' in set(subnet).intersection(compare_args):
#            self.assertEqual(sorted(compare_args['dns_nameservers']),
#                             sorted(subnet['dns_nameservers']))
#            del subnet['dns_nameservers'], compare_args['dns_nameservers']
#
#        self._compare_resource_attrs(subnet, compare_args)
#        self.networks_client.delete_network(net_id)
#        self.networks.pop()
#        self.subnets.pop()
#            
#from nose.tools import set_trace;set_trace()
