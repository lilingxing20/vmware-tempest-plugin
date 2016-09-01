#!/usr/bin/env python
# coding=utf-8

'''
Author      : lixx (https://github.com/lilingxing20)
Created Time: Fri 26 Aug 2016 11:51:05 AM CST
File Name   : test_tokens.py
Description : 
'''

from tempest.common.utils import data_utils
from vmware_tempest_plugin.tests.api.identity import base

class TokensTestVmwareJSON(base.VmwareBaseIdentityV2AdminTest):

    def test_get_tokens(self):
        # get a token by username and password
        user_name = data_utils.rand_name(name='user')
        user_password = data_utils.rand_password()
        # first:create a tenant
        tenant_name = data_utils.rand_name(name='tenant')
        tenant = self.tenants_client.create_tenant(name=tenant_name)['tenant']
        tenant_id = tenant['id']
        # Delete the tenant at the end of the test
        self.addCleanup(self.tenants_client.delete_tenant, tenant_id)
        # second:create a user
        user = self.users_client.create_user(name=user_name,
                                             password=user_password,
                                             tenantId=tenant_id,
                                             email='')['user']
        user_id = user['id']
        # Delete the user at the end of the test
        self.addCleanup(self.users_client.delete_user, user_id)
        # then get a token for the user
        body = self.token_client.auth(
                user=user_name,
                password=user_password,
                tenant=tenant_name)
        self.assertEqual(body['token']['tenant']['name'],
                         tenant_name)
        # Perform GET Token
        token_id = body['token']['id']
        token_details = self.client.show_token(token_id)['access']
        self.assertEqual(token_id, token_details['token']['id'])
        self.assertEqual(user_id, token_details['user']['id'])
        self.assertEqual(user_name, token_details['user']['name'])
        self.assertEqual(tenant_name,
                         token_details['token']['tenant']['name'])
        # then delete the token
        self.client.delete_token(token_id)


#from nose.tools import set_trace;set_trace()
