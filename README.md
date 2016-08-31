# vmware-tempest-plugin

git clone http://git.openstack.org/openstack/tempest
cd tempest
python setup.py install

vim site-packages/tempest-12.1.1.dev312-py2.7.egg-info/entry_points.txt
[tempest.test_plugins]
plugin_name = vmware_tempest_plugin.plugin:VmwarePlugin

