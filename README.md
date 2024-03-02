TO DO list:

Done:

Get VM information
Restart VM
Delete VM
Add new VM with automatic VM folder creation based on the customer name

Remaining:

create a dedicated network (if not already created), and place the VM in this folder without specifying an IP address (use DHCP).
If not the first VM, set internal IP addresses for communication within the dedicated network.

Distribute VMs automatically across available hosts:

This might involve logic to select a host based on current load or available resources

Ensure the customer can manage their VMs but not access others'.

Install-Module -Name "VMware.PowerCLI"  -Scope AllUsers

Set-PowerCLIConfiguration -InvalidCertificateAction Ignore -Confirm:$false

dot source the script

. .\api.ps1

Get-VMInfo -vmName "docker"

Restart-SelectedVM -vmName "docker"

Add-NewVM -customerName "CustomerA" -vmName "CustomerA_docker" -template "docker-template" -datastore "esxi3-datastore1"

Remove-SelectedVM -vmName "new-docker"


python app.py

http://localhost:5000/



### 1. Dockerfile

Create a Dockerfile that builds an image containing PowerShell, VMware PowerCLI, Python, and Flask. Given that VMware PowerCLI runs on PowerShell and PowerShell is available on Linux, you can start with a Linux base image. Here's an example Dockerfile:

```Dockerfile
# Use a base image with PowerShell
FROM mcr.microsoft.com/powershell:latest

# Install Python and pip
RUN apt-get update && \
    apt-get install -y python3 python3-pip

# Install VMware PowerCLI
RUN pwsh -Command "Set-PSRepository -Name PSGallery -InstallationPolicy Trusted; Install-Module -Name VMware.PowerCLI -Scope AllUsers -Confirm:$false"

# Set the working directory in the container
WORKDIR /app

# Copy the Flask app to the container
COPY . /app

# Install Python dependencies
RUN pip3 install Flask

# Expose the port the app runs on
EXPOSE 5000

# Command to run the app
CMD [ "python3", "app.py" ]
```

### 2. Flask Application

Ensure your Flask application (`app.py`) and all its dependencies (e.g., the HTML templates and the PowerShell scripts it calls) are located within the same directory as your Dockerfile. This directory structure ensures everything is copied into the Docker image.

### 3. Building and Running the Docker Container

After creating your Dockerfile, build the Docker image by running the following command in the same directory as your Dockerfile:

```bash
docker build -t flask-powercli-app .
```

Once the image is built, you can run a container from this image with:

```bash
docker run -p 5000:5000 flask-powercli-app
```

This command maps port 5000 of the container to port 5000 on your host, allowing you to access the Flask application by navigating to `http://localhost:5000` in a web browser.

### Considerations

- **PowerCLI Configuration**: Running VMware PowerCLI commands may require additional configuration, such as connecting to your VMware vCenter or ESXi host. You might need to modify your application to handle these connections securely, possibly involving passing credentials securely to the container.
- **Security**: Be cautious with how you handle VMware credentials and other sensitive information, ensuring they are not hard-coded into your Dockerfile or Flask application.
- **Permissions**: Depending on what your PowerShell scripts are doing, you might run into permission issues. Ensure that the user within the Docker container has the necessary permissions to perform the required actions.
- **Networking**: The Docker container needs network access to your VMware vCenter or ESXi hosts. Ensure that the container's network is configured correctly to allow this connectivity.
