import os


def uninstall(service_name):
    # Stop and disable the service
    os.system(f'sudo systemctl stop {service_name}')
    os.system(f'sudo systemctl disable {service_name}')

    # Remove the service file
    service_file = f'/etc/systemd/system/{service_name}.service'
    os.remove(service_file)


service_name = 'PowerfullBackground'
uninstall(service_name)
print('Uninstalled PowerfullBackground')
