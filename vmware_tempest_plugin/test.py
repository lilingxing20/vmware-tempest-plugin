#!/usr/bin/env python
# coding=utf-8

'''
Author      : lixx (https://github.com/lilingxing20)
Created Time: Thu 01 Sep 2016 01:23:50 PM CST
File Name   : test.py
Description : 
'''
import six

from tempest import test

from vmware_tempest_plugin import clients


class VmwareBaseTestCase(test.BaseTestCase):
    vmware_client_manager = clients.ManagerVmware

    @classmethod               
    def setup_credentials(cls):
        """Allocate credentials and create the client managers from them.
                               
        For every element of credentials param function creates tenant/user,
        Then it creates client manager for that credential.
                               
        Network related tests must override this function with
        set_network_resources() method, otherwise it will create
        network resources(network resources are created in a later step).
        """
        super(VmwareBaseTestCase, cls).setup_credentials()

        for credentials_type in cls.credentials:
            # This may raise an exception in case credentials are not available
            # In that case we want to let the exception through and the test
            # fail accordingly 
            if isinstance(credentials_type, six.string_types):
                vmware_manager = cls.get_vmware_client_manager(
                    credential_type=credentials_type)
                setattr(cls, 'vmware_os_%s' % credentials_type, vmware_manager)
                # Setup some common aliases
                # TODO(andreaf) The aliases below are a temporary hack
                # to avoid changing too much code in one patch. They should
                # be removed eventually
                if credentials_type == 'primary':
                    cls.vmware_os = cls.vmware_manager = cls.vmware_os_primary
                if credentials_type == 'admin':
                    cls.vmware_os_adm = cls.admin_vmware_manager = cls.vmware_os_admin
                if credentials_type == 'alt':
                    cls.alt_vmware_manager = cls.vmware_os_alt
            elif isinstance(credentials_type, list):
                vmware_manager = cls.get_vmware_client_manager(roles=credentials_type[1:],
                                                 force_new=True)
                setattr(cls, 'vmware_os_roles_%s' % credentials_type[0], vmware_manager)

    @classmethod    
    def get_vmware_client_manager(cls, credential_type=None, roles=None,
                                 force_new=None):
        """Returns an OpenStack client manager
                    
        Returns an OpenStack client manager based on either credential_type
        or a list of roles. If neither is specified, it defaults to
        credential_type 'primary'
        :param credential_type: string - primary, alt or admin
        :param roles: list of roles
                    
        :returns: the created client manager
        :raises skipException: if the requested credentials are not available
        """         
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
        return cls.vmware_client_manager(credentials=creds.credentials,
                                  service=cls._service)

