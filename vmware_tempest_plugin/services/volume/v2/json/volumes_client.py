#!/usr/bin/env python
# coding=utf-8

'''
Author      : lixx (https://github.com/lilingxing20)
Created Time: Thu 06 Oct 2016 04:44:00 PM CST
File Name   : volumes_client.py
Description : 
'''

from vmware_tempest_plugin.services.volume.base import base_volumes_client

class VmwareVolumesClient(base_volumes_client.VmwareBaseVolumesClient):
    """Client class to send CRUD Volume V1 API requests"""
    api_version = "v2"
    create_resp = 202

