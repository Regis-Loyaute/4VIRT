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

function Remove-SelectedVM {
    param(
        [string]$vmName
    )
    $vm = Get-VM -Name $vmName
    if ($vm) {
        # Check if the VM is powered on and stop it before deletion
        if ($vm.PowerState -eq "PoweredOn") {
            Stop-VM -VM $vm -Confirm:$false -Kill
        }

        # Remove the VM and delete its files from the datastore
        Remove-VM -VM $vm -DeletePermanently -Confirm:$false
        Write-Output "VM and its files have been deleted from the datastore."
    } else {
        Write-Output "VM not found."
    }
}

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

# Function to add a new VM with customer-specific logic
function Add-NewVM {
    param(
        [string]$customerName,
        [string]$vmName,
        [string]$template,
        [string]$datastore,
        [string]$ip = $null
    )

    # Check for the customer folder; create if it doesn't exist
    $customerFolder = Get-Folder -Name $customerName -ErrorAction SilentlyContinue
    if (-not $customerFolder) {
        $customerFolder = New-Folder -Name $customerName -Location (Get-Folder 'vm')
        # Assume the dedicated network is created here for the customer if required
    }

    # Select the host and template
    $vmHost = Get-VMHost | Sort-Object -Property MemoryUsageGB -Descending | Select-Object -First 1
    $templateVM = Get-Template -Name $template
    $datastore = Get-Datastore -Name $datastore

    # Create the VM
    $newVM = New-VM -Name $vmName -Template $templateVM -VMHost $vmHost -Datastore $datastore -Location $customerFolder

    # VM count and network adjustment logic omitted for brevity
    # Additional configurations, such as network settings, should go here

    Write-Output "New VM added: $vmName"
}