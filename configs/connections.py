import paramiko
from configs.configurations import server_auth



class LX:

    def create_ssh_connection(self):
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(**server_auth)
   
    # def run_test_ssh_1(self):
    #     command = 'cd snap; ./2.sh'
    #     stdin, stdout, stderr = self.ssh.exec_command(command)
    #     output = stdout.read().decode()
    #     return output
    
    # def run_test_ssh_2(self):
    #     command = 'ls'
    #     stdin, stdout, stderr = self.ssh.exec_command(command)
    #     output = stdout.read().decode()
    #     return output
    
    def run_tests_LX(self):
        command = 'cd ..; cd usr; cd bin; ./run-tests'
        stdin, stdout, stderr = self.ssh.exec_command(command)
        output = stdout.read().decode()
        command = 'cd ..; cd tmp; cat ./test.log'
        stdin, stdout, stderr = self.ssh.exec_command(command)
        output = stdout.read().decode()
        return output
    
    def run_tests_FPGA(self):
        command = 'cd ..; cd usr; cd bin; ./test-fpga 1 0'
        stdin, stdout, stderr = self.ssh.exec_command(command)
        output = stdout.read().decode()
        return output
    
    def run_hw_test_Singletone(self):
        command = 'cd ..; cd usr; cd bin; ./test-fpga 0 2'
        stdin, stdout, stderr = self.ssh.exec_command(command)
        output = stdout.read().decode()
        return output
    
    def run_hw_test_Loopback(self):
        command = 'cd ..; cd usr; cd bin; ./test-fpga 0 1'
        stdin, stdout, stderr = self.ssh.exec_command(command)
        output = stdout.read().decode()
        return output

    def run_hw_test_Freqresp(self):
        command = 'cd ..; cd usr; cd bin; ./test-fpga 0 3'
        stdin, stdout, stderr = self.ssh.exec_command(command)
        output = stdout.read().decode()
        return output

    def run_hw_test_Phaseshift(self):
        command = 'cd ..; cd usr; cd bin; ./test-fpga 0 4'
        stdin, stdout, stderr = self.ssh.exec_command(command)
        output = stdout.read().decode()
        return output

    def close_ssh_connection(self):
        self.ssh.close

    