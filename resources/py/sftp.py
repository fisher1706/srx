import paramiko

def sftpConnect(my_username,my_key_filename,my_host='sftp.storeroomlogix.com',my_port=22):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(my_host, port=my_port, username=my_username, key_filename=my_key_filename, timeout=20)
    sftp = ssh.open_sftp()
    return sftp

def sftpPutFile(sftp,localpath,remotepath):
    file = sftp.put(localpath,remotepath)
    return file

def sftpClose(sftp):
    sftp.close()

def sftpGetFile(sftp,remotepath,localpath):
    file = sftp.get(remotepath,localpath)
    return file

def sftpListFolder(sftp,path):
    list = sftp.listdir(path)
    return list

def sftpCompareLists(first_list,second_list):
    result = list(set(first_list) - set(second_list))
    return result

