from flask import Flask, render_template, request
import subprocess

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/execute', methods=['POST'])
def execute():
    action = request.form['action']
    vm_name = request.form.get('vmName', '')
    template = request.form.get('template', '')
    vm_host = request.form.get('vmHost', '')
    datastore = request.form.get('datastore', '')

    # The path to your PowerShell script
    ps_script_path = ".\\api.ps1"

    # Define the PowerShell command to dot-source your script and call its function
    if action == 'display':
        ps_command = f". '{ps_script_path}'; Get-VMInfo -vmName '{vm_name}'"
    elif action == 'delete':
        ps_command = f". '{ps_script_path}'; Remove-SelectedVM -vmName '{vm_name}'"
    elif action == 'restart':
        ps_command = f". '{ps_script_path}'; Restart-SelectedVM -vmName '{vm_name}'"
    elif action == 'add':
        ps_command = f". '{ps_script_path}'; Add-NewVM -vmName '{vm_name}' -template '{template}' -vmHost '{vm_host}' -datastore '{datastore}'"
    else:
        return "Invalid action"

    # Execute the PowerShell command
    process = subprocess.run(["powershell", "-Command", ps_command], capture_output=True, text=True)
    output = process.stdout or "Failed to execute command"
    return f"<pre>{output}</pre>"

if __name__ == '__main__':
    app.run(debug=True)