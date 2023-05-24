from pysnmp.hlapi import *
from .constants import COMMUNITY_STRING, MAC_OID, PORT_OID, OID_LEN

class SNMPSwitch:
    def __init__(self, ip_address):
        self.ip_address = ip_address

    def get_snmp_data(self):
        data = {}

        # Perform SNMP walk
        iterator = nextCmd(
            SnmpEngine(),
            CommunityData(COMMUNITY_STRING),
            UdpTransportTarget((self.ip_address, 161)),
            ContextData(),
            ObjectType(ObjectIdentity(MAC_OID)),
            ObjectType(ObjectIdentity(PORT_OID)),
            lexicographicMode=False
        )

        for errorIndication, errorStatus, errorIndex, varBinds in iterator:
            if errorIndication:
                print('SNMP error: %s' % errorIndication)
                return None
            elif errorStatus:
                print(
                    'SNMP error: %s at %s' % (
                        errorStatus.prettyPrint(),
                        errorIndex and varBinds[int(errorIndex) - 1] or '?'
                    )
                )
                return None
            else:
                for varBind in varBinds:
                    data[str(varBind[0])] = str(varBind[1])

        return data
    
    def get_mac_address_table(self):
        mac_address_table = {}

        snmp_data = self.get_snmp_data()
        
        for entry in snmp_data:
            oid_prefix = entry[:OID_LEN]
            oid_suffix = entry[OID_LEN+1:]
 
            if oid_suffix not in mac_address_table:
                mac_address_table[oid_suffix] = {}

            if oid_prefix == MAC_OID:
                # Convert each ASCII value to hexadecimal and format it
                hex_groups = [hex(ord(byte))[2:].zfill(2) for byte in snmp_data[entry]]

                mac_address_table[oid_suffix]['address'] = ":".join(hex_groups)
            elif oid_prefix == PORT_OID:
                mac_address_table[oid_suffix]['port'] = snmp_data[entry]

        return mac_address_table
    
    def sort_mac_address_table(self, mac_address_table):
        sorted_mac_address_table = dict(sorted(mac_address_table.items(), key = lambda x: int(x[1]['port'])))
        return sorted_mac_address_table

    def print_mac_address_table(self, sorted=False):
        mac_address_table = self.get_mac_address_table()

        if sorted:
            mac_address_table = self.sort_mac_address_table(mac_address_table)

        if mac_address_table:
            print(f"MAC Address Table for Switch {self.ip_address}:")
            print("{:<20} {:<10}".format("MAC Address", "Port"))
            print("-" * 35)
            for entry in mac_address_table:
                print("{:<20} {:<10}".format(mac_address_table[entry]['address'], mac_address_table[entry]['port']))
        else:
            print(f"Failed to retrieve MAC Address Table for Switch {self.ip_address}")
        
        print()


    def search_mac(self, mac_address):
        mac_address_table = self.get_mac_address_table()
        mac_address = mac_address.lower()

        if mac_address_table:
            print(f"Searching MAC Address {mac_address} on Switch {self.ip_address}:")
            print("-" * 35)

            for entry in mac_address_table:
                if mac_address_table[entry]['address'] == mac_address:
                    print(f"Mac address {mac_address} found on port {mac_address_table[entry]['port']}!")
                    print("-" * 35)
                    print()
                    return mac_address_table[entry]['port']
            
            print(f"Mac address {mac_address} was not found!")
        else:
            print(f"Failed to retrieve MAC Address Table for Switch {self.ip_address}")
        
        print()