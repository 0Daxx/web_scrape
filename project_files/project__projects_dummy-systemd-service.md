Dummy Systemd Service
beginner

Dummy Systemd Service
=====================

Create a long-running systemd service that logs to a file.

Start building, submit solution and get feedback from the community.

Start Working
The goal of this project is to get familiar with `systemd`; creating and enabling a service, checking the status, keeping an eye on the logs, starting and stopping the service, etc.

Requirements
------------

Create a script called `dummy.sh` that keeps running forever and writes a message to the log file every 10 seconds simulating an application running in the background. Here is an example script:

bash

```
#!/bin/bashwhile true; do  echo "Dummy service is running..." >> /var/log/dummy-service.log  sleep 10done
```

Create a systemd service `dummy.service` that should start the app automatically on boot and keep it running in the background. If the service fails for any reason, it should automatically restart.

You should be able to `start`, `stop`, `enable`, `disable`, check the `status` of the service, and check the logs i.e. following commands should be available for the service:

bash

```
# Interacting with the servicesudo systemctl start dummysudo systemctl stop dummysudo systemctl enable dummysudo systemctl disable dummysudo systemctl status dummy# Check the logssudo journalctl -u dummy -f
```

---

After completing this project, you will have a good understanding of systemd, creating custom services, managing existing services, debugging issues, and more.

