Install-Module -Name "VMware.PowerCLI"  -Scope AllUsers

Set-PowerCLIConfiguration -InvalidCertificateAction Ignore -Confirm:$false

dot source the script

. .\api.ps1

Get-VMInfo -vmName "docker"

Restart-SelectedVM -vmName "docker"

Add-NewVM -vmName "new-docker" -template "docker-template" -vmHost "esxi2.4virt.lan" -datastore "esxi2-datastore1"

Remove-SelectedVM -vmName "new-docker"


python app.py

http://localhost:5000/
