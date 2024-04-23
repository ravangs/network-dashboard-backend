import json
import logging
from jinja2 import Template
from netmiko import ConnectHandler
import os
import time

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def configure_router(router_json):
    cwd = os.getcwd()
    templates_path = os.path.join(cwd, 'network_dashboard', 'configuration', 'templates')
    
    config = router_json

    device = {
        'device_type': 'cisco_ios',
        'host': config['management_ip'],
        'username': config['username'],
        'password': config['password'],
    }

    try:
        with ConnectHandler(**device) as net_connect:
            net_connect.enable()
            net_connect.config_mode()  # Explicitly enter configuration mode

            # Configuring Interfaces
            if config['interfaces']:
                logging.info("Configuring interfaces")
                template_path = os.path.join(templates_path, 'interfaces.j2')
                with open(template_path) as file:
                    interface_template = Template(file.read())
                interface_config = interface_template.render(interfaces=config['interfaces'])
                output = net_connect.send_config_set(interface_config.splitlines())
                logging.info("Interface Configuration Output: \n" + output)
            time.sleep(5)

            # Configuring BGP
            if config['bgp']:
                logging.info("Configuring BGP")
                template_path = os.path.join(templates_path, 'bgp.j2')
                with open(template_path) as file:
                    bgp_template = Template(file.read())
                bgp_config = bgp_template.render(bgp=config['bgp'])
                output = net_connect.send_config_set(bgp_config.splitlines())
                logging.info("BGP Configuration Output: \n" + output)
            time.sleep(5)

            # Configuring OSPF
            if config['ospf']:
                logging.info("Configuring OSPF")
                template_path = os.path.join(templates_path, 'ospf.j2')
                with open(template_path) as file:
                    ospf_template = Template(file.read())
                ospf_config = ospf_template.render(ospf=config['ospf'])
                output = net_connect.send_config_set(ospf_config.splitlines())
                logging.info("OSPF Configuration Output: \n" + output)
            time.sleep(5)

            # Configuring IPv6
            if config['ipv6']:
                logging.info("Configuring IPv6")
                template_path = os.path.join(templates_path, 'ipv6.j2')
                with open(template_path) as file:
                    ipv6_template = Template(file.read())
                ipv6_config = ipv6_template.render(ipv6_configs=config['ipv6'])
                output = net_connect.send_config_set(ipv6_config.splitlines())
                logging.info("IPv6 Configuration Output: \n" + output)
            time.sleep(5)

            # Configuring SNMP
            logging.info("Configuring SNMP")
            template_path = os.path.join(templates_path, 'snmp.j2')
            with open(template_path) as file:
                snmp_template = Template(file.read())
            snmp_config = snmp_template.render(host=config['management_ip'])
            output = net_connect.send_config_set(snmp_config.splitlines())
            logging.info("SNMP Configuration Output: \n" + output)
            time.sleep(5)

    except Exception as e:
        logging.error("Failed to connect or configure the router", exc_info=True)

