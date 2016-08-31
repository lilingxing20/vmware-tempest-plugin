#!/usr/bin/env python
# coding=utf-8

'''
Author      : lixx (https://github.com/lilingxing20)
Created Time: Fri 26 Aug 2016 01:48:47 PM CST
File Name   : vmware_plugin.py
Description : 
'''

import os

from tempest import config
from tempest.test_discover import plugins
from vmware_tempest_plugin import config as config_vmware


class VmwarePlugin(plugins.TempestPlugin):

    def load_tests(self):
        base_path = os.path.split(os.path.dirname(
            os.path.abspath(__file__)))[0]
        test_dir = "vmware_tempest_plugin/tests"
        full_test_dir = os.path.join(base_path, test_dir)
        return full_test_dir, base_path

    def register_opts(self, conf):
        config.register_opt_group(
            conf,
            config_vmware.service_available_group,
            config_vmware.ServiceAvailableGroup)
        config.register_opt_group(
            conf,
            config_vmware.volume_vmware_group,
            config_vmware.VolumeVmwareGroup)

    def get_opt_lists(self):
        return [
                (config_vmware.service_available_group.name,
                 config_vmware.VolumeVmwareGroup),
                (config_vmware.volume_vmware_group.name,
                 config_vmware.VolumeVmwareGroup)
                ]

