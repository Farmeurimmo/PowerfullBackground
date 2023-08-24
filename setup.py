import os
import subprocess


def create_systemd_service(service_name, script_path, script_directory):
    subprocess.call(['pip', 'install', '-r', 'requirements.txt'])
    service_content = f'''[Unit]
Description={service_name}
After=network.target

[Service]
ExecStart=/usr/bin/python {script_path}
WorkingDirectory={script_directory}
Type=simple
Restart=always
RestartSec=3
StandardOutput={script_directory}/output.log
StandardError={script_directory}/error.log

[Install]
WantedBy=multi-user.target
'''

    service_file = f'/etc/systemd/system/{service_name}.service'

    with open(service_file, 'w') as file:
        file.write(service_content)

    os.chmod(service_file, 0o644)

    os.system(f'sudo systemctl enable {service_name}')
    os.system(f'sudo systemctl start {service_name}')


service_name = 'PowerfullBackground'
script_directory = os.getcwd()
script_path = script_directory + '/src/powerfullbackground/Main.py'

create_systemd_service(service_name, script_path, script_directory)
