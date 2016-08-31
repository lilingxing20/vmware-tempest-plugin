#!/usr/bin/env python
# coding=utf-8

'''
Author      : lixx (https://github.com/lilingxing20)
Created Time: Mon 29 Aug 2016 04:13:43 PM CST
File Name   : base_volumes_client.py
Description : 
'''

from tempest.services.volume.base import base_volumes_client

class BaseVolumesVmwareClient(base_volumes_client.BaseVolumesClient):
    def __init__(self, auth_provider, service, region,
                 default_volume_size=1,
                 default_volume_type=None,
                 **kwargs):
        super(BaseVolumesVmwareClient, self).__init__(
                auth_provider, service, region, default_volume_size, **kwargs)
        if default_volume_type:
            self.default_volume_type = default_volume_type

    def create_volume(self, **kwargs):
        """Creates a new Volume.

        Available params: see http://developer.openstack.org/
                              api-ref-blockstorage-v2.html#createVolume
        """
        if 'size' not in kwargs:
            kwargs['size'] = self.default_volume_size
        if 'volume_type' not in kwargs:
            kwargs['volume_type'] = self.default_volume_type
        post_body = json.dumps({'volume': kwargs})
        resp, body = self.post('volumes', post_body)
        body = json.loads(body)
        self.expected_success(self.create_resp, resp.status)
        return rest_client.ResponseBody(resp, body)

