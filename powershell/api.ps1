param(
    [string]$vcServer,
    [string]$username,
    [string]$password
)

# Check if all necessary parameters are provided
if (-not $vcServer -or -not $username -or -not $password) {
    Write-Output "Error: Please provide vCenter server address, username, and password."
    exit
}

# Connect to the vCenter server
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
        if ($vm.PowerState -eq "PoweredOn") {
            Stop-VM -VM $vm -Confirm:$false -Kill
        }
        Remove-VM -VM $vm -DeletePermanently -Confirm:$false
        Write-Output "VM and its files have been deleted from the datastore."
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

function Add-NewVM {
    param(
        [string]$customerName,
        [string]$vmName,
        [string]$template,
        [string]$datastore,
        [string]$ip = $null
    )

    $customerFolder = Get-Folder -Name $customerName -ErrorAction SilentlyContinue
    if (-not $customerFolder) {
        $customerFolder = New-Folder -Name $customerName -Location (Get-Folder 'vm')
    }

    $vmHost = Get-VMHost | Sort-Object -Property MemoryUsageGB | Select-Object -First 1
    
    $templateVM = Get-Template -Name $template -ErrorAction SilentlyContinue
    if (-not $templateVM) {
        Write-Output "Template '$template' not found. Exiting."
        return
    }

    $datastore = Get-Datastore -Name $datastore -ErrorAction SilentlyContinue
    if (-not $datastore) {
        Write-Output "Datastore '$datastore' not found. Exiting."
        return
    }

    if (-not $vmHost) {
        Write-Output "VMHost not found. Exiting."
        return
    }

    # Create or retrieve the distributed switch port group for the customer
    $networkName = "$customerName-network"
    $dvs = Get-VDSwitch -Name "DSwitch" -ErrorAction SilentlyContinue
    if (-not $dvs) {
        Write-Output "Distributed vSwitch 'DSwitch' not found. Exiting."
        return
    }
    
    $dvPortGroup = Get-VDPortgroup -VDSwitch $dvs -Name $networkName -ErrorAction SilentlyContinue
    if (-not $dvPortGroup) {
        $dvPortGroup = New-VDPortgroup -VDSwitch $dvs -Name $networkName
    }

    # Create the new VM
    $newVM = New-VM -Name $vmName -Template $templateVM -VMHost $vmHost -Datastore $datastore -Location $customerFolder

    # Change the network adapter of the VM to the newly created network
    $vmNetworkAdapter = Get-NetworkAdapter -VM $newVM
    Set-NetworkAdapter -NetworkAdapter $vmNetworkAdapter -Portgroup $dvPortGroup -Confirm:$false

    # Power on the VM
    Start-VM -VM $newVM -Confirm:$false

    Write-Output "New VM added and powered on: $vmName. Network adapter is connected to $networkName. Please connect using Remote Desktop."
}