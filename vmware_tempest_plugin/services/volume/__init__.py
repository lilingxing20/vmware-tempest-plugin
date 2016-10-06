#!/usr/bin/env python
# coding=utf-8

'''
Author      : lixx (https://github.com/lilingxing20)
Created Time: Mon 29 Aug 2016 05:30:37 PM CST
File Name   : __init__.py
Description : 
'''

from vmware_tempest_plugin.services.volume import v1
from vmware_tempest_plugin.services.volume import v2

__all__ = ['v1', 'v2']
