"""show_lisp_named_services.py

    * show lisp {lisp_id} instance-id {instance_id} named-services map-cache
    * show lisp locator-table {locator_table} instance-id {instance_id} named-services map-cache
    * show lisp instance-id {instance_id} named-services map-cache
    * show lisp {lisp_id} instance-id {instance_id} named-services map-cache {eid_prefix}
    * show lisp locator-table {locator_table} instance-id {instance_id} named-services map-cache {eid_prefix}
    * show lisp instance-id {instance_id} named-services map-cache {eid_prefix}
"""

# Metaparser
from genie.metaparser import MetaParser
from genie.metaparser.util.schemaengine import Optional

from genie.libs.parser.iosxe.show_lisp_super import (ShowLispIpMapCachePrefixSuperParser,
                                                     ShowLispMapCacheSuperParser)


# ========================================================================
# Parser for 'show lisp instance-id <instance_id> named-services map-cache'
# ========================================================================
class ShowLispNamedServicesMapCache(ShowLispMapCacheSuperParser):
    """Parser for:
        * show lisp {lisp_id} instance-id {instance_id} named-services map-cache
        * show lisp locator-table {locator_table} instance-id {instance_id} named-services map-cache
        * show lisp instance-id {instance_id} named-services map-cache
    """

    cli_command = [
        'show lisp {lisp_id} instance-id {instance_id} named-services map-cache',
        'show lisp locator-table {locator_table} instance-id {instance_id} named-services map-cache',
        'show lisp instance-id {instance_id} named-services map-cache'
    ]

    def cli(self, command=None, output=None, lisp_id=None, locator_table=None,
            instance_id=None, **kwargs):
        if output is None:
            output = self.device.execute(command)

        return super().cli(output=output)


# ========================================================================
# Schema for 'show lisp instance-id <instance_id> named-services map-cache <eid_prefix>'
# ========================================================================
class ShowLispNamedServicesMapCachePrefixSchema(MetaParser):
    """Schema for named-services map-cache prefix commands."""

    schema = {
        'lisp_id': {
            int: {
                'instance_id': {
                    int: {
                        'eid_table': str,
                        'entries': int,
                        'eid_prefix': str,
                        'uptime': str,
                        'expires': str,
                        'via': str,
                        Optional('site'): str,
                        'sources': str,
                        'state': str,
                        'last_modified': str,
                        'map_source': str,
                        Optional('activity'): str,
                        Optional('packets_out'): int,
                        Optional('packets_out_bytes'): int,
                        Optional('encap'): str,
                        'locators': {
                            str: {
                                'uptime': str,
                                'state': str,
                                'priority': int,
                                'weight': int,
                                'encap_iid': str,
                                Optional('state_change_time'): str,
                                Optional('state_change_count'): int,
                                Optional('route_reachability_change_time'): str,
                                Optional('route_reachability_change_count'): int,
                                Optional('priority_change'): str,
                                Optional('weight_change'): str,
                                Optional('rloc_probe_sent'): str
                            }
                        }
                    }
                }
            }
        }
    }


# ========================================================================
# Parser for 'show lisp instance-id <instance_id> named-services map-cache <eid_prefix>'
# ========================================================================
class ShowLispNamedServicesMapCachePrefix(
        ShowLispNamedServicesMapCachePrefixSchema,
        ShowLispIpMapCachePrefixSuperParser):
    """Parser for:
        * show lisp {lisp_id} instance-id {instance_id} named-services map-cache {eid_prefix}
        * show lisp locator-table {locator_table} instance-id {instance_id} named-services map-cache {eid_prefix}
        * show lisp instance-id {instance_id} named-services map-cache {eid_prefix}
    """

    cli_command = [
        'show lisp {lisp_id} instance-id {instance_id} named-services map-cache {eid_prefix}',
        'show lisp locator-table {locator_table} instance-id {instance_id} named-services map-cache {eid_prefix}',
        'show lisp instance-id {instance_id} named-services map-cache {eid_prefix}'
    ]

    def cli(self, command=None, output=None, lisp_id=None, instance_id=None,
            eid_prefix=None, locator_table=None, **kwargs):
        if output is None:
            output = self.device.execute(command)

        return super().cli(eid_prefix, output=output, lisp_id=lisp_id,
                           instance_id=instance_id, locator_table=locator_table)
