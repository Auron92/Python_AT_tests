import getpass
import paramiko

username = input('username:')
password = getpass.getpass(prompt="Password:")

server_auth = {
    'hostname': "PC-ALS-LNX-06",
    'username': username,
    'password': password,
    'port': 22
}

try:
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(**server_auth)
except paramiko.AuthenticationException as e:
    print("Authentification failed!")
else:
    commands = ['ls',
                'cd snap; pwd',
                'pwd',
                'cd snap; ./2.sh'
    ]

    for command in commands:
        stdin, stdout, stderr = ssh.exec_command(command)
        output = stdout.read().decode()
        print(output)

    ssh.close


