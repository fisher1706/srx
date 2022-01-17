import pysftp
import os


class Utils:

    @staticmethod
    def generate_url(uri, **kwargs):
        for arg in kwargs:
            uri += '/' + str(kwargs[arg])
        return uri

    @staticmethod
    def cleaner(dir_path):
        for _file in os.listdir(dir_path):
            os.remove(dir_path + _file)
            print(f'file: {_file} - deleted')

    @staticmethod
    def read_rtf_file(dir_path, file_name):
        data_out = {}

        with open(dir_path + file_name, 'r') as _file:
            data = _file.read().split('~')

        for index, item in enumerate(data):
            data_out.update({index: item})
            print(index, ':', item)

        return data_out

    @staticmethod
    def create_rtf_file(dir_path, file_name, data_write):
        data_str = '~'.join(data_write.values())
        print(f"file: {file_name} - created")

        with open(dir_path + file_name, "w") as _file:
            _file.write(data_str)

    @staticmethod
    def download_sftp_files(host, username, password, local_path, remote_path):
        srv = pysftp.Connection(host=host, username=username, password=password)
        srv.chdir(remotepath=remote_path)

        try:
            for _file in srv.listdir(remote_path):
                srv.get(remotepath=remote_path + _file, localpath=local_path + _file)
                print(f'file download: {_file}')
        except Exception as e:
            print(e)
        srv.close()

    @staticmethod
    def get_count_sftp_files(host, username, password, remote_path):
        count = 0

        srv = pysftp.Connection(host=host, username=username, password=password)
        srv.chdir(remotepath=remote_path)

        for _file in srv.listdir(remote_path):
            print(f'sftp file found: {_file}')
            count += 1
        srv.close()

        return count

    @staticmethod
    def upload_sftp_files(host, username, password, local_path, remote_path):
        srv = pysftp.Connection(host=host, username=username, password=password)
        srv.chdir(remotepath=remote_path)

        try:
            for _file in os.listdir(local_path):
                srv.put(localpath=local_path + _file)
                print(f'file upload: {_file}')
        except Exception as e:
            print(e)
        srv.close()

    @staticmethod
    def get_data_order_infor(order_no, data_infor):
        return [data for data in data_infor if str (order_no) == str(data.get ('orderno'))][0]
