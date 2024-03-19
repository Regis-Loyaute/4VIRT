from flask import Flask, render_template, request
import subprocess

app = Flask(__name__)

@app.route('/')
def home():
    # Renders the home page that includes the form for user inputs
    return render_template('index.html')

@app.route('/execute', methods=['POST'])
def execute():
    # Collect action type and parameters from the form
    action = request.form['action']
    vm_name = request.form.get('vmName', '')
    template = request.form.get('template', '')
    vm_host = request.form.get('vmHost', '')
    datastore = request.form.get('datastore', '')
    vc_server = request.form.get('vcServer', '')
    username = request.form.get('username', '')
    password = request.form.get('password', '')
    customer_name = request.form.get('customerName', '')

    # The path to your PowerShell script
    ps_script_path = ".\\api.ps1"

    # Construct PowerShell command based on the action selected
    if action == 'display':
        ps_command = (f". '{ps_script_path}' -vcServer '{vc_server}' -username '{username}' -password '{password}'; "
                      f"Get-VMInfo -vmName '{vm_name}'")
    elif action == 'delete':
        ps_command = (f". '{ps_script_path}' -vcServer '{vc_server}' -username '{username}' -password '{password}'; "
                      f"Remove-SelectedVM -vmName '{vm_name}'")
    elif action == 'restart':
        ps_command = (f". '{ps_script_path}' -vcServer '{vc_server}' -username '{username}' -password '{password}'; "
                      f"Restart-SelectedVM -vmName '{vm_name}'")
    elif action == 'add':
        ps_command = (f". '{ps_script_path}' -vcServer '{vc_server}' -username '{username}' -password '{password}'; "
                      f"Add-NewVM -customerName '{customer_name}' -vmName '{vm_name}' -template '{template}' "
                      f"-vmHost '{vm_host}' -datastore '{datastore}'")
    else:
        return "Invalid action"

    # Execute the PowerShell command
    process = subprocess.run(["powershell", "-Command", ps_command], capture_output=True, text=True)
    output = process.stdout or process.stderr or "Failed to execute command"
    return f"<pre>{output}</pre>"

if __name__ == '__main__':
    app.run(debug=True)
