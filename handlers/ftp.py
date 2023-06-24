from ftplib import FTP


class FTPHandler:
    ftp = FTP()
    path_to_logs = 'SCUM/Saved/SaveFiles/Logs'

    def __init__(self, host, port, user, password) -> None:
        self.host = host
        self.port = port
        self.user = user
        self.password = password

    def connect_and_login(self):
        self.ftp.connect(host=self.host, port=self.port)
        self.ftp.login(user=self.user, passwd=self.password)

    def close_connection(self):
        self.ftp.close()

    # Setters
    def set_current_directory_to_log_directory(self):
        self.ftp.cwd(self.path_to_logs)

    # Getters
    def get_current_log_filename_by_type(self, log_type):
        all_logs_by_type = []
        all_logs = self.ftp.mlsd()

        for log in all_logs:
            if log_type in log[0]:
                all_logs_by_type.append(log[0])        

        return all_logs_by_type[-1]
    
    
    
    def save_current_log_by_type(self, current_log_filename):
        with open('logs/%s'%current_log_filename, 'wb') as f:
            self.ftp.retrbinary('RETR %s'%current_log_filename, f.write)