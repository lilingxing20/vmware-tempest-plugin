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
import tempest.test

from vmware_tempest_plugin.tests import clients

CONF = config.CONF


class BaseVolumeVmwareTest(tempest.test.BaseTestCase):
    """Base test case class for all Cinder API tests."""

    _api_version = 2
    credentials = ['primary']
    client_vmware_manager = clients.ManagerVmware

    @classmethod
    def skip_checks(cls):
        super(BaseVolumeVmwareTest, cls).skip_checks()

        if not CONF.service_available.cinder:
            skip_msg = ("%s skipped as Cinder is not available" % cls.__name__)
            raise cls.skipException(skip_msg)
        if cls._api_version == 1:
            if not CONF.volume_feature_enabled.api_v1:
                msg = "Volume API v1 is disabled"
                raise cls.skipException(msg)
        elif cls._api_version == 2:
            if not CONF.volume_feature_enabled.api_v2:
                msg = "Volume API v2 is disabled"
                raise cls.skipException(msg)
        elif cls._api_version == 3:
            if not CONF.volume_feature_enabled.api_v3:
                msg = "Volume API v3 is disabled"
                raise cls.skipException(msg)
        else:
            msg = ("Invalid Cinder API version (%s)" % cls._api_version)
            raise exceptions.InvalidConfiguration(message=msg)

    @classmethod
    def get_client_vmware_manager(cls, credential_type=None, roles=None,
                           force_new=None):
        if all([roles, credential_type]):
            msg = "Cannot get credentials by type and roles at the same time"
            raise ValueError(msg)
        if not any([roles, credential_type]):
            credential_type = 'primary'
        cred_provider = cls._get_credentials_provider()
        if roles:
            for role in roles:
                if not cred_provider.is_role_available(role):
                    skip_msg = (
                        "%s skipped because the configured credential provider"
                        " is not able to provide credentials with the %s role "
                        "assigned." % (cls.__name__, role))
                    raise cls.skipException(skip_msg)
            params = dict(roles=roles)
            if force_new is not None:
                params.update(force_new=force_new)
            creds = cred_provider.get_creds_by_roles(**params)
        else:
            credentials_method = 'get_%s_creds' % credential_type
            if hasattr(cred_provider, credentials_method):
                creds = getattr(cred_provider, credentials_method)()
            else:
                raise lib_exc.InvalidCredentials(
                    "Invalid credentials type %s" % credential_type)
        return cls.client_vmware_manager(credentials=creds.credentials,
                                            service=cls._service)

    @classmethod
    def setup_credentials(cls):
        cls.set_network_resources()
        super(BaseVolumeVmwareTest, cls).setup_credentials()

        for credentials_type in cls.credentials:
            # This may raise an exception in case credentials are not available
            # In that case we want to let the exception through and the test
            # fail accordingly
            if isinstance(credentials_type, six.string_types):
                vmware_manager = cls.get_client_vmware_manager(
                    credential_type=credentials_type)
                setattr(cls, 'os_vmware_%s' % credentials_type, vmware_manager)
                # Setup some common aliases
                # TODO(andreaf) The aliases below are a temporary hack
                # to avoid changing too much code in one patch. They should
                # be removed eventually
                if credentials_type == 'primary':
                    cls.os_vmware = cls.vmware_manager = cls.os_vmware_primary
                if credentials_type == 'admin':
                    cls.os_vmware_adm = cls.admin_manager = cls.os_vmware_admin
                if credentials_type == 'alt':
                    cls.alt_vmware_manager = cls.os_vmware_alt
            elif isinstance(credentials_type, list):
                vmware_manager = cls.get_client_vmware_manager(roles=credentials_type[1:],
                                                 force_new=True)
                setattr(cls, 'os_roles_vmware_%s' % credentials_type[0], manager)

    @classmethod
    def setup_clients(cls):
        super(BaseVolumeVmwareTest, cls).setup_clients()
        cls.servers_client = cls.os.servers_client
        cls.compute_networks_client = cls.os.compute_networks_client
        cls.compute_images_client = cls.os.compute_images_client

        if cls._api_version == 1:
            cls.snapshots_client = cls.os.snapshots_client
            cls.volumes_client = cls.os.volumes_client
            cls.backups_client = cls.os.backups_client
            cls.volume_services_client = cls.os.volume_services_client
            cls.volumes_extension_client = cls.os.volumes_extension_client
            cls.availability_zone_client = (
                cls.os.volume_availability_zone_client)
        else:
            cls.snapshots_client = cls.os.snapshots_v2_client
            cls.volumes_client = cls.os.volumes_v2_client
            cls.backups_client = cls.os.backups_v2_client
            cls.volumes_extension_client = cls.os.volumes_v2_extension_client
            cls.availability_zone_client = (
                cls.os.volume_v2_availability_zone_client)
        cls.volumes_vmware_client = cls.os_vmware.voluem_vmware_client

    @classmethod
    def resource_setup(cls):
        super(BaseVolumeVmwareTest, cls).resource_setup()

        cls.snapshots = []
        cls.volumes = []
        cls.image_ref = CONF.compute.image_ref
        cls.flavor_ref = CONF.compute.flavor_ref
        cls.build_interval = CONF.volume.build_interval
        cls.build_timeout = CONF.volume.build_timeout
        cls.default_volume_type = CONF.volume_vmware.volume_type

        if cls._api_version == 1:
            # Special fields and resp code for cinder v1
            cls.special_fields = {'name_field': 'display_name',
                                  'descrip_field': 'display_description'}
        else:
            # Special fields and resp code for cinder v2
            cls.special_fields = {'name_field': 'name',
                                  'descrip_field': 'description'}

    @classmethod
    def resource_cleanup(cls):
        cls.clear_snapshots()
        cls.clear_volumes()
        super(BaseVolumeVmwareTest, cls).resource_cleanup()

    @classmethod
    def create_volume(cls, **kwargs):
        """Wrapper utility that returns a test volume."""
        #from nose.tools import set_trace;set_trace()
        name = data_utils.rand_name(cls.__name__ + '-Volume')
        name_field = cls.special_fields['name_field']
        kwargs[name_field] = name

        kwargs['volume_type'] = cls.default_volume_type

        volume = cls.volumes_vmware_client.create_volume(**kwargs)['volume']

        cls.volumes.append(volume)
        waiters.wait_for_volume_status(cls.volumes_vmware_client,
                                       volume['id'], 'available')
        return volume

    @classmethod
    def create_snapshot(cls, volume_id=1, **kwargs):
        """Wrapper utility that returns a test snapshot."""
        snapshot = cls.snapshots_client.create_snapshot(
            volume_id=volume_id, **kwargs)['snapshot']
        cls.snapshots.append(snapshot)
        waiters.wait_for_snapshot_status(cls.snapshots_client,
                                         snapshot['id'], 'available')
        return snapshot

    # NOTE(afazekas): these create_* and clean_* could be defined
    # only in a single location in the source, and could be more general.

    @classmethod
    def delete_volume(cls, client, volume_id):
        """Delete volume by the given client"""
        client.delete_volume(volume_id)
        client.wait_for_resource_deletion(volume_id)

    @classmethod
    def clear_volumes(cls):
        for volume in cls.volumes:
            try:
                cls.volumes_client.delete_volume(volume['id'])
            except Exception:
                pass

        for volume in cls.volumes:
            try:
                cls.volumes_client.wait_for_resource_deletion(volume['id'])
            except Exception:
                pass

    @classmethod
    def clear_snapshots(cls):
        for snapshot in cls.snapshots:
            try:
                cls.snapshots_client.delete_snapshot(snapshot['id'])
            except Exception:
                pass

        for snapshot in cls.snapshots:
            try:
                cls.snapshots_client.wait_for_resource_deletion(snapshot['id'])
            except Exception:
                pass

    @classmethod
    def create_server(cls, name, **kwargs):
        tenant_network = cls.get_tenant_network()
        body, _ = compute.create_test_server(
            cls.os,
            tenant_network=tenant_network,
            name=name,
            **kwargs)
        return body


class BaseVolumeAdminVmwareTest(BaseVolumeVmwareTest):
    """Base test case class for all Volume Admin API tests."""

    credentials = ['primary', 'admin']

    @classmethod
    def setup_clients(cls):
        super(BaseVolumeAdminVmwareTest, cls).setup_clients()

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
        cls.admin_volume_vmware_client = cls.volumes_vmware_client

    @classmethod
    def resource_setup(cls):
        super(BaseVolumeAdminVmwareTest, cls).resource_setup()

        cls.qos_specs = []
        cls.volume_types = []

    @classmethod
    def resource_cleanup(cls):
        cls.clear_qos_specs()
        super(BaseVolumeAdminVmwareTest, cls).resource_cleanup()
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
