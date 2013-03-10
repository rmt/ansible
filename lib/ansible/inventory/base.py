"""
InventoryBase serves the dual purpose of documenting the external interface
for the Inventory, and providing some helper functions that can be used
from any inventory implementation that inherits it.
"""

class InventoryBase(object):
    def __init__(self, hostfile):
        """
        :type hostfile: string
        :param hostfile: the argument to the -i CLI argument
        """

    def list_hosts(self, pattern):
        """
        If the inventory implementation caches host information, be sure to
        empty the cache if the subset changes.  *restriction* and
        *also_restriction* should be applied to the full list after caching.

        *pattern* is typically a hostname or group pattern to match.

        :type pattern: string
        :param pattern: a string containing a pattern to match
        :rtype: list of strings
        :returns: return a list of host names matching the current search criteria
        """
        return []

    def subset(self, subset_pattern):
        """
        :type subset_pattern: string
        :param subset_pattern: a subset pattern to apply when returning hosts
        """

    def restrict_to(self, host_list):
        """restrict by hostname list (used by the playbook implementation)

        :type host_list: list of strings
        :param host_list: a list of hostnames
        """

    def lift_restriction(self):
        """remove restrictions"""

    def also_restrict_to(self, host_list):
        """restrict by hostname list (also used by the playbook implementation)

        :type host_list: list of strings
        :param host_list: a list of hostnames
        """

    def get_variables(self, hostname):
        """return variables for this host

        :type hostname: string
        :param hostname: hostname whose variables should be returned
        :rtype: dict
        :returns: a dictionary of variable keys and values
        """
        return {}

    def lift_also_restriction(self):
        """remove also_restrictions"""

    def groups_for_host(self, hostname):
        """
        :type hostname: string
        :param hostname: a single hostname
        :rtype: list of strings
        :returns: a list of groups for which the given hostname is a member
        """
        return []

    def groups_list(self): # FIXME: poorly named, as it returns a dict
        """Returns all the groups and the hostnames they contain

        :rtype: dictionary of string: [list of strings]
        :returns: a dictionary mapping a group name to a list of hostname
        """
        return {}

    def add_host(self, hostname, hostvars=None, groupnames=None, port=None):
        """Add a new host and assign it to the given groups.

        If the host already exists, an exception will be thrown.
        Groups will be created if they don't exist.

        :type hostname: string
        :param hostname: hostname of host to add
        :type hostvars: dict
        :param hostvars: variables for this host
        :type groupnames: list of strings
        :param groupnames:
        :throws: KeyError ??
        """
        raise NotImplementedError

    def add_host_to_group(self, hostname, groupname):
        """Add a host to a group, creating the group if necessary.

        :type hostname: string
        :param hostname: hostname of existing host
        :type groupname: string
        :param groupname: name of group
        """
        raise NotImplementedError
