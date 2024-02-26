from pyVim.connect import SmartConnect, Disconnect
import ssl

# Disable SSL certificate verification (not recommended for production)
ssl._create_default_https_context = ssl._create_unverified_context

# vCenter connection details
vcenter_ip = 'vcsa.4virt.lan'
username = 'administrator@vphsere.local'
password = '4VIRT.lan'

# Connect to vCenter
si = SmartConnect(host=vcenter_ip, user=username, pwd=password, sslContext=ssl._create_default_https_context())

# Get vcenter content object
content = si.RetrieveContent()

# Find the datacenter
datacenter = content.rootFolder.childEntity[0]

# Find the VM folder
vm_folder = datacenter.vmFolder

# List of VM templates
vm_templates = []

# Iterate over all entities in the VM folder
for entity in vm_folder.childEntity:
    # Check if the entity is a VM template
    if entity.config.template:
        vm_templates.append(entity.name)

# Print the names of all VM templates
for template in vm_templates:
    print(template)

# Disconnect from vCenter
Disconnect(si)