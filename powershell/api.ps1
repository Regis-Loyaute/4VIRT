# Connect to the vCenter server
$vcServer = 'vcsa.4virt.lan'
$username = 'administrator@vphsere.local'
$password = '4VIRT.lan'
Connect-VIServer -Server $vcServer -User $username -Password $password

# Function to display selected VM information
function Get-VMInfo {
    param(
        [string]$vmName
    )
    $vm = Get-VM -Name $vmName
    if ($vm) {
        $vmView = $vm | Get-View
        $status = if ($vm.PowerState -eq "PoweredOn") { "On" } else { "Off" }
        $lastBackupDate = $vmView.CustomFields | Where-Object { $_.Key -eq "LastBackupDate" } | Select-Object -ExpandProperty Value
        $lastBackupDate = if ($lastBackupDate) { $lastBackupDate } else { "N/A" }

        [PSCustomObject]@{
            Name           = $vm.Name
            IP             = $vm.Guest.IPAddress
            Status         = $status
            LastBackupDate = $lastBackupDate
        }
    } else {
        Write-Output "VM not found."
    }
}

# Function to delete a VM
function Remove-SelectedVM {
    param(
        [string]$vmName
    )
    $vm = Get-VM -Name $vmName
    if ($vm) {
        Remove-VM -VM $vm -Confirm:$false
        Write-Output "VM deleted."
    } else {
        Write-Output "VM not found."
    }
}

# Function to restart a VM
function Restart-SelectedVM {
    param(
        [string]$vmName
    )
    $vm = Get-VM -Name $vmName
    if ($vm) {
        Restart-VMGuest -VM $vm -Confirm:$false
        Write-Output "VM is restarting."
    } else {
        Write-Output "VM not found."
    }
}

# Function to add a new VM
function Add-NewVM {
    param(
        [string]$vmName,
        [string]$template,
        [string]$vmHost,
        [string]$datastore,
        [string]$ip = $null
    )
    $templateVM = Get-Template -Name $template
    $vmHost = Get-VMHost -Name $vmHost
    $datastore = Get-Datastore -Name $datastore
    $newVM = New-VM -Name $vmName -Template $templateVM -VMHost $vmHost -Datastore $datastore

    if ($ip) {
        # Additional configuration for setting IP can be added here
    }

    Write-Output "New VM added: $vmName"
}