--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------

* iosxe
    * Added ShowPlatformHardwareFedSwitchActiveForwardInterfacePcap
        * show platform hardware fed switch active forward interface {interface} pcap {pcap_path} number {number} flowid {flowid}
        * show platform hardware fed switch {switch} forward interface {interface} pcap {pcap_path} number {number} flowid {flowid}
    * Modified PingMpls
        * Added support for 'ping mpls pseudowire {addr} {vc_id} reply {reply_option}'
        * Added support for 'ping mpls tp tunnel-tp {tunnel_tp_id} lsp working channel ip repeat {count}'
    * Added ShowPlatformSoftwareFedQosInterfaceEgressTypeQueueNpdDetailed
        * Added schema and parser for 'show platform software fed {switch} qos interface {interface} egress type-queue npd detailed'
    * Added ShowPlatformSoftwareFedQosInterfaceEgressTypeQueueNpiDetailed
        * Added schema and parser for 'show platform software fed {switch} qos interface {interface} egress type-queue npi detailed'
    * Added ShowPlatformSoftwareFedQosInterfaceEgressTypeQueueSdkDetailed
        * Added schema and parser for 'show platform software fed {switch} qos interface {interface} egress type-queue sdk detailed'
    * Added ShowPlatformSoftwareFedSwitchPuntAclStatistics
        * Added schema and parser for 'show platform software fed switch punt acl statistics'
    * Added ShowPlatformSoftwareFedSwitchIfmInterfaceName parser
        * Added rv1 parser for 'show platform software fed switch 1 ifm interface name' command.
    * Added ShowLicenseUsage parser in show_license.py
        * Added schema and parser for cli 'show license usage'
    * Added ShowPlatformHardwareQfpActiveInfrastructureBqsScheduleOutputDefaultInterface
        * Added schema and parser for 'show platform hardware qfp active infrastructure bqs schedule output default interface {interface}'
    * Added ShowCryptoIkev2StatsExchange
        * Added schema and parser for 'show crypto ikev2 stats exchange'
    * Added ShowLacpMultiChassisLoadBalanceGroupGroupId
        * Added schema and parser for 'show lacp multi-chassis load-balance group {group_id}'
    * Added ShowPlatformSoftwareEssFpActiveDrl
        * Added schema and parser for 'show platform software ess FP active drl'
    * Added NslookupDomain
        * Added schema and parser for 'nslookup {domain}'
    * Added TestCryptoMasterKeyPresent
        * Added schema and parser for 'show crypto master-key'
    * Added ShowSystemInsecureProfile
        * Added schema and parser for 'show system insecure-profile'
    * Added ShowBfdNeighbors
        * Added 'show bfd neighbors'
    * Added ShowPlatformHardwareFedSwitchFwdAsicInsightIpsecSecurityEngine
        * Added schema and parser for 'show platform hardware fed {switch} fwd-asic insight ipsec_security_engine'
    * Added ShowPlatformHardwareFedSwitchFwdAsicInsightIpsecSessionOid
        * Added schema and parser for 'show platform hardware fed {switch} fwd-asic insight ipsec_session_oid'
    * Added ShowPlatformHardwareFedSwitchFwdAsicInsightIpsecTunnels
        * Added schema and parser for 'show platform hardware fed {switch} fwd-asic insight ipsec_tunnels'
    * Added ShowPlatformHardwareFedSwitchFwdAsicInsightIpsecSecurityAssociation
        * Added schema and parser for 'show platform hardware fed {switch} fwd-asic insight ipsec_security_association'
    * Added ShowLacpMultiChassisLoadBalancePortChannelId
        * Added schema and parser for 'show lacp multi-chassis load-balance port-channel {id}'
    * Added ShowPlatformSoftwareAccessListRpActiveStatistics
        * Added schema and parser for 'show platform software access-list RP active statistics'
    * Added ShowPolicyFirewallStatsVrfGlobal
        * Added schema and parser for 'show policy-firewall stats vrf global'


--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* iosxe
    * Modified ShowPlatformSoftwareFedSwitchActiveFnfAttachPointsDump
        * 'show platform software fed switch active fnf attach-points dump'
    * Modified ShowMonitorCaptureBuffer
        * Added new CLI 'show monitor capture {capture_name} buffer brief' to show brief output of capture buffer.
    * Modified ShowPlatformSoftwareFedSecurityStormControlIfId
        * Added Optional key 'storm_control_not_configured' to schema and parser to indicate if storm control is not configured for the interface.
    * Modified ShowPlatformSoftwareFedSecurityStormControlIfId parser
        * Added new regex to capture the new output of the command "show platform software fed security storm-control if-id" command. The new output has an additional column "Storm Control Action" which is being captured in the new regex.
    * Modified ShowPlatformSoftwareFedSwitchIfmInterfaceName
        * Added mac_port_oid as Optional in the schema as it is not present in all the outputs of the command "show platform software fed switch 1 ifm interface name".
    * Modified ShowPlatformSoftwareFedIpsecCounter parser
        * Added new regex to capture the new output of the command "show platform software fed ipsec if-id <ifid>"
    * Modified ShowRedundancyStates
        * Added new extra parameters to verify.
    * Removed rv1 ShowPolicyMapInterface
        * Removed rv1 schema and parser for 'show policy-map interface' (will use original version of the parser)
        * After removing rv1 schema and parser, the output of 'show policy-map interface' will be same as before
        * queue limit and random_detect in ms/bytes are not supported in original version
    * Added fix for ShowPlatformSoftwareFedActiveAclInfoDbDetail parser.
        * Added this fix to support multiple all_entries.
    * Modified ShowLine
        * Updated overruns regex to accept negative values, fixing silent drop of TTY/VTY lines on long-running devices whose overrun counters have wrapped to a negative integer.
    * Created rv1 ShowMplsL2TransportSummary
        * Created rv1 schema and parser for 'show mpls l2transport summary'
        * The output of 'show mpls l2transport summary' will be same as before, but can show more different destination IPs dictionary with different vc status and active vc count
    * Added fix for ShowRunInterface parser.
        * Added this fix to support multiple entries.
    * Modified ShowStackPower
        * Updated regex pattern to match 3rd power supply in the stack.
    * Modified ShowSmartPowerChildren
        * Extended role pattern to support IP Phone devices, interface keyword, and AIR-AP wireless devices with "NA" usage values.

* iosxr
    * Modified AdminShowDiagChassis
        * Widened the PID and VID regexes from ``[a-zA-Z0-9\-]+`` to ``\S+`` so that values containing ``/`` (e.g. ``N/A``) are captured. Previously, devices reporting ``PID N/A`` / ``VID N/A`` (such as third-party IOS XR chassis) caused ``SchemaMissingKeyError Missing keys [['vid'], ['pid']]`` because the fields were silently dropped from the parsed dict.
    * Modified rv1 ShowDiagDetails
        * Widened the PID regex from ``[\w\.-]+`` to ``\S+`` for the same reason, so IDPROM items reporting ``PID N/A`` populate the ``pid`` field instead of being silently omitted.
    * Modified rv1 ShowDiagDetails
        * Widened the IDPROM header regex from ``IDPROM\s+\-\s+`` to ``IDPROM\d*\s+\-\s+`` so headers like ``0/SYNC0-GNSS_LC-IDPROM0 -`` open a new section instead of leaking fields into the previous one.
    * Modified ShowControllersOpticsObservableInfo
        * Modified schema and parser for 'show controllers optics {port} observable-info' command.
        * Modified schema and parser for 'show controllers optics * observable-info' command.
        * Update the parsed structure to contain 'cmd_status' field with value 'Available' for each section under 'observable_info' for each port. This indicates that the information for that section is available and has been parsed successfully.
    * Modified ShowPlatform
        * Modified parser for 'show platform' command for new State

* parser
    * Modified get_parser
        * Added abstract deprecation context to parser lookup results so


--------------------------------------------------------------------------------
                                    Modified                                    
--------------------------------------------------------------------------------

* iosxe
    * Modified ShowLispServiceMapCache
        * Added support for `show lisp all instance-id {instance_id} named-services map-cache`.
        * Added support for named-services DN map-cache output under the service map-cache schema.
    * Added ShowLispNamedServicesMapCache
        * Added under the named-services command family.
        * show lisp {lisp_id} instance-id {instance_id} named-services map-cache
        * show lisp instance-id {instance_id} named-services map-cache
    * Added ShowLispNamedServicesMapCachePrefix
        * Added under the named-services command family.
        * show lisp {lisp_id} instance-id {instance_id} named-services map-cache {eid_prefix}
        * show lisp instance-id {instance_id} named-services map-cache {eid_prefix}
        * show lisp locator-table {locator_table} instance-id {instance_id} named-services map-cache {eid_prefix}
    * Modified ShowLispDatabaseEid
        * Updated regex pattern `p4` to parse named-services EID prefixes without mask syntax.
        * Added named-services database EID unit test coverage under the existing parser.
    * Modified ShowLispDatabaseSuperParserSchema
        * Changed schema key `mask` from required to Optional for named-services database entries.
    * Modified ShowLispDatabaseSuperParser
        * Updated regex pattern `p1` to accept `DN` mapping databases and `N/A` EID-tables.
        * Updated regex pattern `p3` to parse named-services EIDs without mask syntax.
        * Updated EID handling logic to store maskless named-services entries correctly.
    * Added named-services unit test coverage to existing parser classes
        * ShowLispService
        * ShowLispInstanceIdService
        * ShowLispServiceDatabase
        * ShowLispDatabaseEid


