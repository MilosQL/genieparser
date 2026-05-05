from genie.metaparser import MetaParser
from genie.metaparser.util.schemaengine import Any
import re
from lxml import etree

# ======================================================
# Schema for 'show router arp dynamic'
# ======================================================

class ShowRouterArpDynamicSchema(MetaParser):
	"""Schema for show router arp dynamic"""
	schema = {
		'router': {
			Any(): {
				"entries" : int,
				'ip_address': {
					Any(): {
						'interface': str,
						'mac_add': str,
						'expiry': str,
						'type':str
					}
				}
			}
		}
	}

class ShowRouterArpDynamic(ShowRouterArpDynamicSchema):
	""" Parser for show router arp dynamic """
	cli_command = 'show router arp dynamic'

	def cli(self, output=None):

		if output is None:
			out = self.device.execute(self.cli_command)
		else:
			out = output
		
		parsed_dict = {}
		
		
		#ARP Table Router: (Base) 
		#    or
		#ARP Table (Router: Base) 
		p0 = re.compile(r'^ARP Table.*[\s(](?P<router>[^)]+)\)$')
		#
		# Note: By examining the YANG model and its type definitions, we can see that `router-name` may contain spaces. 
		
		#No. of ARP Entries: 4
		p1 = re.compile(r'^No. of ARP Entries: (?P<entries>\d+)$')

		#10.4.1.1         00:fe:c8:ff:db:6d 02h34m12s Dyn[I] To-ASR5.5K
		p2 = re.compile(r'^(?P<ip_address>\S+) +(?P<mac_add>\S+) +(?P<expiry>\S+) +(?P<type>\S+) +(?P<interface>\S+)$')
		
		for line in out.splitlines():
			line= line.strip()

			#ARP Table Router: (Base)
			m = p0.match(line)
			if m:
				router_dict = parsed_dict.setdefault('router', {}).setdefault(m.groupdict()['router'], {})
				continue

			#No. of ARP Entries: 4
			m = p1.match(line)
			if m:
				router_dict["entries"] = int(m.groupdict()['entries'])
				continue
			
			#10.4.1.1         00:fe:c8:ff:db:6d 02h34m12s Dyn[I] To-ASR5.5K
			m = p2.match(line)
			if m:
				group = m.groupdict()
				ip_address = group['ip_address']
				mac_add = group['mac_add']
				expiry = group['expiry']
				type_mac = group['type']
				interface = group['interface']
				
				interface_dict = router_dict.setdefault('ip_address', {}).setdefault(ip_address, {})
				
				interface_dict["interface"] = interface
				interface_dict["mac_add"] = mac_add
				interface_dict["expiry"] = expiry
				interface_dict["type"] = type_mac
				continue

		return parsed_dict

	def yang(self, output=None):

		if output is None:
			filter_xml = """
			<filter xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
				<state xmlns="urn:nokia.com:sros:ns:yang:sr:state">
					<router>
						<interface>
							<ipv4>
								<neighbor-discovery>
									<neighbor/>
								</neighbor-discovery>
							</ipv4>
						</interface>
					</router>
				</state>
			</filter>
			"""
			ele_filter = etree.fromstring(filter_xml)
			response = self.device.nc.get(filter=ele_filter)
			output = response.data_xml

		parsed_dict = {'router': {}}

		# Handle strings vs bytes safely for lxml
		if isinstance(output, str):
			root = etree.fromstring(output.encode('utf-8'))
		else:
			root = etree.fromstring(output)

		ns = {'sros': 'urn:nokia.com:sros:ns:yang:sr:state'}

		# Iterate hierarchically: Router -> Interface -> Neighbor
		for router in root.xpath('.//sros:router', namespaces=ns):
			router_name = router.findtext('sros:router-name', namespaces=ns)
			
			if not router_name:
				continue

			router_dict = {
				'entries': 0,
				'ip_address': {}
			}

			for interface in router.xpath('.//sros:interface', namespaces=ns):
				# Grab the interface name once per interface, not once per neighbor
				intf_name = interface.findtext('sros:interface-name', namespaces=ns)

				for nbr in interface.xpath('.//sros:ipv4/sros:neighbor-discovery/sros:neighbor', namespaces=ns):
					typ = nbr.findtext('sros:type', namespaces=ns)

					# Optional filter: skip non-dynamic entries immediately
					if typ != 'dynamic':
						continue

					ip = nbr.findtext('sros:ipv4-address', namespaces=ns)
					mac = nbr.findtext('sros:mac-address', namespaces=ns)

					seconds = int(nbr.findtext('sros:timer', namespaces=ns))
					# Accoding to the YANG model, the maximum allowed value 
					# for seconds is 65535, which is less than 19h
					h = seconds // 3600
					m = (seconds % 3600) // 60
					s = seconds % 60 
					timer = f"{h:02d}h{m:02d}m{s:02d}s"

					if ip:
						router_dict['ip_address'][ip] = {
							'interface': intf_name,
							'mac_add': mac,
							'expiry': timer,
							'type': 'Dyn[I]'  # Hardcoded since we already filtered for 'dynamic'
						}
						router_dict['entries'] += 1

			# Only add the router to the final dict if it actually has valid neighbors
			if router_dict['ip_address']:
				parsed_dict['router'][router_name] = router_dict

		return parsed_dict
