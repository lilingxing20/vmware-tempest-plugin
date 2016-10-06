#!/usr/bin/env python
# coding=utf-8

'''
Author      : lixx (https://github.com/lilingxing20)
Created Time: Mon 29 Aug 2016 03:17:05 PM CST
File Name   : base.py
Description : 
'''
import six

from tempest.common import compute
from tempest.common.utils import data_utils
from tempest.common import waiters
from tempest import config
from tempest import exceptions
from tempest.lib.common.utils import test_utils

from tempest.api.volume import base

from vmware_tempest_plugin import test as vmware_test
from vmware_tempest_plugin import clients

CONF = config.CONF


class VmwareBaseVolumeTest(vmware_test.VmwareBaseTestCase,
                           base.BaseVolumeTest):
    """Base test case class for all Cinder API tests."""

    _api_version = 2
    credentials = ['primary']

    @classmethod
    def setup_credentials(cls):
        cls.set_network_resources()
        super(VmwareBaseVolumeTest, cls).setup_credentials()

    @classmethod
    def setup_clients(cls):
        super(VmwareBaseVolumeTest, cls).setup_clients()
        if cls._api_version == 1:
            cls.volumes_vmware_client = cls.vmware_os.volumes_vmware_client
        elif cls._api_version == 2:
            cls.volumes_vmware_client = cls.vmware_os.volumes_v2_vmware_client

    @classmethod
    def create_volume(cls, **kwargs):
        """Wrapper utility that returns a test volume."""
        #from nose.tools import set_trace;set_trace()
        name = data_utils.rand_name(cls.__name__ + '-Volume')
        name_field = cls.special_fields['name_field']
        kwargs[name_field] = name

        volume = cls.volumes_vmware_client.create_volume(**kwargs)['volume']

        cls.volumes.append(volume)
        waiters.wait_for_volume_status(cls.volumes_vmware_client,
                                       volume['id'], 'available')
        return volume


class VmwareBaseVolumeAdminTest(VmwareBaseVolumeTest):
    """Base test case class for all Volume Admin API tests."""

    credentials = ['primary', 'admin']

    @classmethod
    def setup_clients(cls):
        super(VmwareBaseVolumeAdminTest, cls).setup_clients()

        if cls._api_version == 1:
            cls.admin_volume_qos_client = cls.os_adm.volume_qos_client
            cls.admin_volume_services_client = \
                cls.os_adm.volume_services_client
            cls.admin_volume_types_client = cls.os_adm.volume_types_client
            cls.admin_volume_client = cls.os_adm.volumes_client
            cls.admin_hosts_client = cls.os_adm.volume_hosts_client
            cls.admin_snapshots_client = cls.os_adm.snapshots_client
            cls.admin_backups_client = cls.os_adm.backups_client
            cls.admin_quotas_client = cls.os_adm.volume_quotas_client

            cls.admin_volume_vmware_client = cls.vmware_os_adm.volumes_vmware_client

        elif cls._api_version == 2:
            cls.admin_volume_qos_client = cls.os_adm.volume_qos_v2_client
            cls.admin_volume_services_client = \
                cls.os_adm.volume_services_v2_client
            cls.admin_volume_types_client = cls.os_adm.volume_types_v2_client
            cls.admin_volume_client = cls.os_adm.volumes_v2_client
            cls.admin_hosts_client = cls.os_adm.volume_hosts_v2_client
            cls.admin_snapshots_client = cls.os_adm.snapshots_v2_client
            cls.admin_backups_client = cls.os_adm.backups_v2_client
            cls.admin_quotas_client = cls.os_adm.volume_quotas_v2_client

            cls.admin_volume_vmware_client = cls.vmware_os_adm.volumes_v2_vmware_client

    @classmethod
    def resource_setup(cls):
        super(VmwareBaseVolumeAdminTest, cls).resource_setup()

        cls.qos_specs = []
        cls.volume_types = []

    @classmethod
    def resource_cleanup(cls):
        cls.clear_qos_specs()
        super(VmwareBaseVolumeAdminTest, cls).resource_cleanup()
        cls.clear_volume_types()

    @classmethod
    def create_test_qos_specs(cls, name=None, consumer=None, **kwargs):
        """create a test Qos-Specs."""
        name = name or data_utils.rand_name(cls.__name__ + '-QoS')
        consumer = consumer or 'front-end'
        qos_specs = cls.admin_volume_qos_client.create_qos(
            name=name, consumer=consumer, **kwargs)['qos_specs']
        cls.qos_specs.append(qos_specs['id'])
        return qos_specs

    @classmethod
    def create_volume_type(cls, name=None, **kwargs):
        """Create a test volume-type"""
        name = name or data_utils.rand_name(cls.__name__ + '-volume-type')
        volume_type = cls.admin_volume_types_client.create_volume_type(
            name=name, **kwargs)['volume_type']
        cls.volume_types.append(volume_type['id'])
        return volume_type

    @classmethod
    def clear_qos_specs(cls):
        for qos_id in cls.qos_specs:
            test_utils.call_and_ignore_notfound_exc(
                cls.admin_volume_qos_client.delete_qos, qos_id)

        for qos_id in cls.qos_specs:
            test_utils.call_and_ignore_notfound_exc(
                cls.admin_volume_qos_client.wait_for_resource_deletion, qos_id)

    @classmethod
    def clear_volume_types(cls):
        for vol_type in cls.volume_types:
            test_utils.call_and_ignore_notfound_exc(
                cls.admin_volume_types_client.delete_volume_type, vol_type)

        for vol_type in cls.volume_types:
            # Resource dictionary uses for is_resource_deleted method,
            # to distinguish between volume-type to encryption-type.
            resource = {'id': vol_type, 'type': 'volume-type'}
            test_utils.call_and_ignore_notfound_exc(
                cls.admin_volume_types_client.wait_for_resource_deletion,
                resource)
