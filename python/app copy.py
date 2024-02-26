from flask import Flask, request, jsonify
import requests
from vmware.vapi.vsphere.client import create_vsphere_client
import logging
from urllib3.exceptions import InsecureRequestWarning

# Configure basic logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)

# Disable SSL warnings (not recommended for production)
requests.packages.urllib3.disable_warnings()

# vSphere connection details
VCENTER_SERVER = 'vcsa.4virt.lan'
VCENTER_USERNAME = 'administrator@vphsere.local'
VCENTER_PASSWORD = '4VIRT.lan'
VCENTER_URL = f'https://{VCENTER_SERVER}/rest'

def get_vsphere_client():
    session = requests.session()
    session.verify = False  # Disable SSL verification for simplicity
    client = create_vsphere_client(server=VCENTER_SERVER, username=VCENTER_USERNAME, password=VCENTER_PASSWORD, session=session)
    return client

from flask import Flask, jsonify
import requests
from vmware.vapi.vsphere.client import create_vsphere_client

app = Flask(__name__)

# Assuming you have defined get_vsphere_client() elsewhere in your code
# This function should authenticate and return a vSphere client instance

# Create a session with SSL verification disabled
session = requests.session()
session.verify = False

# Use the custom session when creating the vSphere client
client = create_vsphere_client(server=VCENTER_SERVER, username=VCENTER_USERNAME, password=VCENTER_PASSWORD, session=session)

@app.route('/vms', methods=['GET'])
def get_all_vms():
    client = get_vsphere_client()
    vms_list = client.vcenter.VM.list()
    vms_info = []

    for vm_summary in vms_list:
        vm = client.vcenter.VM.get(vm_summary.vm)
        vm_power_info = client.vcenter.vm.Power.get(vm_summary.vm)
        vm_info = {
            "Name": vm.name,
            "VM": vm_summary.vm,
            "Status": "On" if vm_power_info.state == "POWERED_ON" else "Off",
            # Additional VM details can be added here
        }
        vms_info.append(vm_info)

    return jsonify(vms_info)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

@app.route('/vm/<vm_name>', methods=['GET'])
def get_vm_by_name(vm_name):
    client = get_vsphere_client()
    vms_list = client.vcenter.VM.list()
    
    for vm_summary in vms_list:
        vm = client.vcenter.VM.get(vm_summary.vm)
        if vm.name.lower() == vm_name.lower():
            vm_power_info = client.vcenter.vm.Power.get(vm_summary.vm)
            vm_info = {
                "Name": vm.name,
                "Status": "On" if vm_power_info.state == "POWERED_ON" else "Off",
                "VM": vm_summary.vm,
            }
            return jsonify(vm_info)
    
    return jsonify({"error": "VM not found"}), 404


@app.route('/vm/delete/<vm_name>', methods=['DELETE'])
def delete_vm_by_name(vm_name):
    client = get_vsphere_client()
    vms_list = client.vcenter.VM.list()
    
    for vm_summary in vms_list:
        vm = client.vcenter.VM.get(vm_summary.vm)
        if vm.name.lower() == vm_name.lower():
            try:
                client.vcenter.VM.delete(vm_summary.vm)
                return jsonify({"message": f"VM '{vm_name}' has been deleted."}), 200
            except Exception as e:
                return jsonify({"error": f"Failed to delete VM '{vm_name}': {str(e)}"}), 500
    
    return jsonify({"error": f"VM '{vm_name}' not found"}), 404


@app.route('/vm/restart/<vm_name>', methods=['POST'])
def restart_vm_by_name(vm_name):
    client = get_vsphere_client()
    vms_list = client.vcenter.VM.list()
    
    for vm_summary in vms_list:
        vm = client.vcenter.VM.get(vm_summary.vm)
        if vm.name.lower() == vm_name.lower():
            try:
                client.vcenter.vm.Power.reset(vm_summary.vm)
                return jsonify({"message": f"VM '{vm_name}' is being restarted."}), 200
            except Exception as e:
                return jsonify({"error": f"Failed to restart VM '{vm_name}': {str(e)}"}), 500
    
    return jsonify({"error": f"VM '{vm_name}' not found"}), 404

@app.route('/create-vm', methods=['POST'])
def create_vm():
    data = request.get_json()
    vm_name = data.get('vm_name')
    template_name = data.get('template_name')

    if not vm_name or not template_name:
        return jsonify({"error": "Both vm_name and template_name are required"}),  400

    try:
        # Find the VM template
        template = client.vcenter.VM.find(template_name)
        if not template:
            return jsonify({"error": "Template not found"}),  404

        # Clone the VM template
        new_vm = template.clone(name=vm_name)

        return jsonify({"message": f"Virtual machine {vm_name} created from template {template_name}"}),  201
    except Exception as e:
        logging.error(f"Error creating VM: {e}")
        return jsonify({"error": "Failed to create VM"}),  500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')