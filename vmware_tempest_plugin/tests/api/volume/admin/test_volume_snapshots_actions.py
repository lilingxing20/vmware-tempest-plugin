#!/usr/bin/env python
# coding=utf-8

'''
Author      : lixx (https://github.com/lilingxing20)
Created Time: Wed 31 Aug 2016 04:13:55 PM CST
File Name   : test_volume_snapshots_actions.py
Description : 
'''

from vmware_tempest_plugin.tests.api.volume import base
from tempest.common.utils import data_utils
from tempest import config
from tempest import test

CONF = config.CONF


class SnapshotsActionsV2Test(base.BaseVolumeAdminVmwareTest):

    @classmethod
    def skip_checks(cls):
        super(SnapshotsActionsV2Test, cls).skip_checks()
        if not CONF.volume_feature_enabled.snapshot:
            raise cls.skipException("Cinder snapshot feature disabled")

    @classmethod
    def setup_clients(cls):
        super(SnapshotsActionsV2Test, cls).setup_clients()
        cls.client = cls.snapshots_client

    @classmethod
    def resource_setup(cls):
        super(SnapshotsActionsV2Test, cls).resource_setup()

        # Create a test shared volume for tests
        vol_name = data_utils.rand_name(cls.__name__ + '-Volume')
        cls.name_field = cls.special_fields['name_field']
        params = {cls.name_field: vol_name}
        cls.volume = cls.create_volume(**params)

        # Create a test shared snapshot for tests
        snap_name = data_utils.rand_name(cls.__name__ + '-Snapshot')
        params = {cls.name_field: snap_name}
        cls.snapshot = cls.create_snapshot(
            volume_id=cls.volume['id'], **params)

    def tearDown(self):
        # Set snapshot's status to available after test
        status = 'available'
        snapshot_id = self.snapshot['id']
        self.admin_snapshots_client.reset_snapshot_status(snapshot_id,
                                                          status)
        super(SnapshotsActionsV2Test, self).tearDown()

    def _create_reset_and_force_delete_temp_snapshot(self, status=None):
        # Create snapshot, reset snapshot status,
        # and force delete temp snapshot
        temp_snapshot = self.create_snapshot(volume_id=self.volume['id'])
        if status:
            self.admin_snapshots_client.\
                reset_snapshot_status(temp_snapshot['id'], status)
        self.admin_snapshots_client.\
            force_delete_snapshot(temp_snapshot['id'])
        self.client.wait_for_resource_deletion(temp_snapshot['id'])

    def _get_progress_alias(self):
        return 'os-extended-snapshot-attributes:progress'

    @test.idempotent_id('3e13ca2f-48ea-49f3-ae1a-488e9180d535')
    def test_reset_snapshot_status(self):
        # Reset snapshot status to creating
        status = 'creating'
        self.admin_snapshots_client.\
            reset_snapshot_status(self.snapshot['id'], status)
        snapshot_get = self.admin_snapshots_client.show_snapshot(
            self.snapshot['id'])['snapshot']
        self.assertEqual(status, snapshot_get['status'])

    @test.idempotent_id('41288afd-d463-485e-8f6e-4eea159413eb')
    def test_update_snapshot_status(self):
        # Reset snapshot status to creating
        status = 'creating'
        self.admin_snapshots_client.\
            reset_snapshot_status(self.snapshot['id'], status)

        # Update snapshot status to error
        progress = '80%'
        status = 'error'
        progress_alias = self._get_progress_alias()
        self.client.update_snapshot_status(self.snapshot['id'],
                                           status=status, progress=progress)
        snapshot_get = self.admin_snapshots_client.show_snapshot(
            self.snapshot['id'])['snapshot']
        self.assertEqual(status, snapshot_get['status'])
        self.assertEqual(progress, snapshot_get[progress_alias])

    @test.idempotent_id('05f711b6-e629-4895-8103-7ca069f2073a')
    def test_snapshot_force_delete_when_snapshot_is_creating(self):
        # test force delete when status of snapshot is creating
        self._create_reset_and_force_delete_temp_snapshot('creating')

    @test.idempotent_id('92ce8597-b992-43a1-8868-6316b22a969e')
    def test_snapshot_force_delete_when_snapshot_is_deleting(self):
        # test force delete when status of snapshot is deleting
        self._create_reset_and_force_delete_temp_snapshot('deleting')

    @test.idempotent_id('645a4a67-a1eb-4e8e-a547-600abac1525d')
    def test_snapshot_force_delete_when_snapshot_is_error(self):
        # test force delete when status of snapshot is error
        self._create_reset_and_force_delete_temp_snapshot('error')

    @test.idempotent_id('bf89080f-8129-465e-9327-b2f922666ba5')
    def test_snapshot_force_delete_when_snapshot_is_error_deleting(self):
        # test force delete when status of snapshot is error_deleting
        self._create_reset_and_force_delete_temp_snapshot('error_deleting')


#class SnapshotsActionsV1Test(SnapshotsActionsV2Test):
#    _api_version = 1