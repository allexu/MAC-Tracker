import click

from .switches import SNMPSwitch
from .constants import IP_LIST

@click.command()
@click.option('-p', '--print', is_flag=True, help='Print the MAC address tables for all switches')
@click.option('-i', '--ip-address', multiple=True, help='Specify IP addresses of switches')
@click.option('-s', '--search', multiple=True, help='Search for MAC addresses in the specified switch(es)')
@click.pass_context
def cli(ctx, print, ip_address, search):
    if not any(ctx.params.values()):
        click.echo(ctx.get_help())
        return

    switches = []
    
    if ip_address:
        for ip in ip_address:
            switches.append(SNMPSwitch(ip))
    else:
        for ip in IP_LIST:
            switches.append(SNMPSwitch(ip))
    
    if print:
        if switches:
            for switch in switches:
                switch.print_mac_address_table(sorted=True)
        else:
            print("No switches specified.")
    
    if search:
        if switches:
            for switch in switches:
                for mac in search:
                    switch.search_mac(mac)
        else:
            print("No switches specified.")