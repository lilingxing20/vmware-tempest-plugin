#!/usr/bin/env python
# coding=utf-8

'''
Author      : lixx (https://github.com/lilingxing20)
Created Time: Fri 26 Aug 2016 11:49:59 AM CST
File Name   : base.py
Description : 
'''

from oslo_log import log as logging
from tempest import config
from tempest.api.identity import base 


CONF = config.CONF
LOG = logging.getLogger(__name__)


class VmwareBaseIdentityV2AdminTest(base.BaseIdentityV2AdminTest):
    @classmethod
    def setup_clients(cls):
        super(VmwareBaseIdentityV2AdminTest, cls).setup_clients()

