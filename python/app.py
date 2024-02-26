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

@app.route('/create_vm', methods=['POST'])
def create_vm():
    """
    Create a new VM from a template.
    Expects JSON in the form of {"vm_name": "new_vm_name", "template_name": "source_template_name"}
    """
    data = request.json
    vm_name = data.get('vm_name')
    template_name = data.get('template_name')

    if not vm_name or not template_name:
        return jsonify({'error': 'Missing vm_name or template_name'}), 400

    try:
        # Assuming you have a function to find the template ID by its name
        template_id = find_template_id_by_name(template_name)

        if not template_id:
            return jsonify({'error': 'Template not found'}), 404

        # Here you'd have logic to create a VM from the template using the vSphere client
        # This is a placeholder for the actual VM creation logic
        # For example: client.vcenter.VM.create(vm_create_spec)
        # Where vm_create_spec is configured with your desired settings, including the template ID
        create_vm_from_template(vm_name, template_id)

        return jsonify({'message': f'VM {vm_name} created successfully from template {template_name}'}), 200
    except Exception as e:
        logging.error(f"Failed to create VM: {e}")
        return jsonify({'error': 'Failed to create VM'}), 500

def find_template_id_by_name(template_name):
    """
    Function to find the VM template ID by its name.
    This is a placeholder; you'll need to implement the logic based on your environment.
    """
    # Placeholder for actual implementation
    # You'd typically search through available templates in your library or inventory
    return 'template_id'

def create_vm_from_template(vm_name, template_id):
    """
    Function to create a VM from a template.
    This is a placeholder; you'll need to implement the logic based on your setup and requirements.
    """
    # Placeholder for actual VM creation logic
    pass

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')