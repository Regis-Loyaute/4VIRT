from flask import Flask, render_template, request, redirect, url_for
import subprocess

app = Flask(__name__)

@app.route('/')
def home():
    # Renders the home page with links to each action
    return render_template('index.html')

@app.route('/display')
def display_vm():
    # Renders the form for displaying VM information
    return render_template('display.html')

@app.route('/delete')
def delete_vm():
    # Renders the form for deleting a VM
    return render_template('delete.html')

@app.route('/restart')
def restart_vm():
    # Renders the form for restarting a VM
    return render_template('restart.html')

@app.route('/add')
def add_vm():
    # Renders the form for adding a new VM
    return render_template('add.html')

@app.route('/execute', methods=['POST'])
def execute():
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

    # Construct the PowerShell command based on the action
    ps_command = ""
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

    # Execute the PowerShell command
    process = subprocess.run(["powershell", "-Command", ps_command], capture_output=True, text=True)
    output = process.stdout or process.stderr or "Failed to execute command"

    # Display the output or redirect to a specific page
    return f"<pre>{output}</pre>"

if __name__ == '__main__':
    app.run(debug=True)
