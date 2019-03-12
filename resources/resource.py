import paramiko

def sftpConnect(my_username,my_key_filename,my_host='sftp.storeroomlogix.com',my_port=22):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(my_host, port=my_port, username=my_username, key_filename=my_key_filename)
    sftp = ssh.open_sftp()
    return sftp

def sftpPutFile(sftp,localpath,remotepath):
    file = sftp.put(localpath,remotepath)
    return file
