from os import walk, remove

LOG_TYPE_ADMIN = 'admin_'
LOG_TYPE_LOGIN = 'login_'

class LogReader:
    path_to_logs='./logs'
    admin_file_position = 1

    def __init__(self) -> None:
        pass

    def remove_old_logs(self, log_type, current_log_filename):
        for (dirpath, dirnames, filenames) in walk(self.path_to_logs):
            for filename in filenames:
                if log_type in filename and current_log_filename != filename:
                    remove('%s/%s'%(self.path_to_logs, filename))
                    self.set_file_position_by_type(log_type=log_type, new_value=0)

    def set_file_position_by_type(self, log_type, new_value):
        if log_type == LOG_TYPE_ADMIN:
            self.admin_file_position = new_value

    def get_file_position_by_type(self, log_type):
        if log_type == LOG_TYPE_ADMIN:
            return self.admin_file_position
        
    def get_messages_by_type(self, log_type, current_log_filename):
        file_position = self.get_file_position_by_type(log_type=log_type)
        file = open('%s/%s'%(self.path_to_logs, current_log_filename), "r")
        messages = []

        for index, line in enumerate(file):
            if index > file_position:
                messages.append(line)
                file_position = index
        
        self.set_file_position_by_type(log_type=log_type, new_value=file_position)

        return messages


    def get_messages_for_discord_by_type(self, log_type, current_log_filename):
        self.remove_old_logs(log_type=log_type, current_log_filename=current_log_filename)

        return self.get_messages_by_type(log_type=log_type, current_log_filename=current_log_filename)