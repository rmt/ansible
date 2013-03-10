# Copyright 2012, Seth Vidal <skvidal@fedoraproject.org>
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.

import ansible

from ansible.callbacks import vv
from ansible.errors import AnsibleError as ae
from ansible.runner.return_data import ReturnData
from ansible.utils import parse_kv, template

class ActionModule(object):
    ''' Create inventory hosts and groups in the memory inventory'''

    ### We need to be able to modify the inventory
    BYPASS_HOST_LOOP = True
    NEEDS_TMPPATH = False

    def __init__(self, runner):
        self.runner = runner

    def run(self, conn, tmp, module_name, module_args, inject, complex_args=None, **kwargs):

        if self.runner.check:
            return ReturnData(conn=conn, comm_ok=True, result=dict(skipped=True, msg='check mode not supported for this module'))

        args = {}
        if complex_args:
            args.update(complex_args)
        args.update(parse_kv(module_args))
        if not 'hostname' in args and not 'name' in args:
            raise ae("'name' is a required argument.")

        result = {'changed': True}

        # Parse out any hostname:port patterns
        new_hostname = args.get('hostname', args.get('name', None))
        vv("creating host via 'add_host': hostname=%s" % new_hostname)

        if ":" in new_hostname:
            new_hostname, new_port = new_hostname.split(":")
            args['ansible_ssh_port'] = new_port

        # create host and get inventory
        inventory = self.runner.inventory
        new_hostvars = {}

        # Add any variables to the new_host
        for k in args.keys():
            if not k in [ 'name', 'hostname', 'groupname', 'groups' ]:
                new_hostvars[k] = args[k]

        groupnames = args.get('groupname', args.get('groups', None))
        if groupnames:
            groupnames_list = groupnames.split(",")
        else:
            groupnames_list = None
        inventory.add_host(new_hostname, new_hostvars, groupnames_list)
        result['changed'] = True

        result['new_groups'] = groupnames_list
        result['new_host'] = new_hostname

        return ReturnData(conn=conn, comm_ok=True, result=result)



