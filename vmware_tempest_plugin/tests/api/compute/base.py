#!/usr/bin/env python
# coding=utf-8

'''
Author      : lixx (https://github.com/lilingxing20)
Created Time: Thu 01 Sep 2016 06:45:02 PM CST
File Name   : base.py
Description : 
'''

import time
from tempest.common import compute
from tempest import config
from tempest.lib.common import api_version_utils
from oslo_log import log as logging
from tempest.api.compute import base

CONF = config.CONF

LOG = logging.getLogger(__name__)


class VmwareBaseV2ComputeTest(base.BaseV2ComputeTest):

    credentials = ['primary', 'admin']

    @classmethod
    def skip_checks(cls):
        super(VmwareBaseV2ComputeTest, cls).skip_checks()

    @classmethod
    def setup_credentials(cls):
        super(VmwareBaseV2ComputeTest, cls).setup_credentials()

    @classmethod
    def setup_clients(cls):
        super(VmwareBaseV2ComputeTest, cls).setup_clients()
              
    @classmethod
    def resource_setup(cls):
        super(VmwareBaseV2ComputeTest, cls).resource_setup()

