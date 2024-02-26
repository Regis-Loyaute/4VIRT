from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim
import ssl

# Disable SSL certificate verification (not recommended for production)
ssl._create_default_https_context = ssl._create_unverified_context

# vCenter connection details
vcenter_ip = 'vcsa.4virt.lan'
username = 'administrator@vphsere.local'
password = '4VIRT.lan'
datacenter = '4virt'
vm_folder = 'vm folder'
# Connect to vCenter
si = SmartConnect(host=vcenter_ip, user=username, pwd=password, sslContext=ssl._create_default_https_context())

# Get vcenter content object
content = si.RetrieveContent()

# Find the datacenter
datacenter = si.content.rootFolder.childEntity[0]

# Find the VM folder
vm_folder = datacenter.vmFolder

# Find the template
template = None
for entity in vm_folder.childEntity:
    if entity.name == 'docker-template':
        template = entity
        break

# Clone the template
if template:
    clone_spec = template.CloneSpec()
    clone_spec.location = template.CloneSpec.RelocateSpec()
    clone_spec.location.pool = datacenter.hostFolder.childEntity[0].resourcePool
    clone_spec.powerOn = False
    clone_spec.template = False
    clone_spec.snapshot = None  # No snapshot required for templates
    clone_task = template.Clone(folder=vm_folder, name='new_vm_name', spec=clone_spec)
    print(f"Cloning VM: {clone_task}")
else:
    print("Template not found")

# Disconnect from vCenter
Disconnect(si)