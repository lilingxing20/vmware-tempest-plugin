#!/usr/bin/env python
# coding=utf-8

'''
Author      : lixx (https://github.com/lilingxing20)
Created Time: Mon 29 Aug 2016 05:30:37 PM CST
File Name   : __init__.py
Description : 
'''

from vmware_tempest_plugin.services.volume.base import base_volumes_client


class VolumesVmwareClient(base_volumes_client.BaseVolumesVmwareClient):
        """Client class to send CRUD Volume V1 API requests"""
