import paramiko
import os

def sftpConnect(my_username,my_key_filename,my_host='sftp.storeroomlogix.com',my_port=22):
    os.umask(0)
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(my_host, port=my_port, username=my_username, key_filename=my_key_filename, timeout=20)
    os.umask(0)
    sftp = ssh.open_sftp()
    return sftp

def sftpPutFile(sftp,localpath,remotepath):
    os.umask(0)
    file = sftp.put(localpath,remotepath)
    return file

def sftpClose(sftp):
    os.umask(0)
    sftp.close()

def sftpGetFile(sftp,remotepath,localpath):
    os.umask(0)
    file = sftp.get(remotepath,localpath)
    return file

def sftpListFolder(sftp,path):
    os.umask(0)
    list = sftp.listdir(path)
    return list

def sftpCompareLists(first_list,second_list):
    os.umask(0)
    result = list(set(second_list) - set(first_list))
    return result