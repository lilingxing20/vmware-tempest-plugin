#!/usr/bin/env python
# coding=utf-8

'''
Author      : lixx (https://github.com/lilingxing20)
Created Time: Fri 26 Aug 2016 01:47:39 PM CST
File Name   : config.py
Description : 
'''

from oslo_config import cfg

_CONF = cfg.CONF

service_available_group = cfg.OptGroup(
    name="service_available",
    title="Available OpenStack Services"
)
ServiceAvailableGroup = [
    cfg.BoolOpt("vmware_tempest_plugin",
                default=True,
                help="Whether or not VMware tests is expected to be available")
]

volume_vmware_group = cfg.OptGroup(name='volume_vmware',
                            title='Block Storage Options')
VolumeVmwareGroup = [
    cfg.StrOpt('volume_type',
               default='vmware',
               help='Default volume type for volumes created by volumes tests'),
    cfg.StrOpt('volume_backend_name',
               default='vmware',
               help='Default volume_backend_name for volume-types created by volume-types tests'),
]


