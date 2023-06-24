import sched, time, argparse

from handlers.ftp import FTPHandler
from handlers.discord import DiscordHandler
from handlers.log_reader import LogReader, LOG_TYPE_ADMIN

def get_command_line_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument("webhook_url", type=str, default="")
    parser.add_argument("host", type=str, default="")
    parser.add_argument("port", type=int, default="00000")
    parser.add_argument("user", type=str, default="")
    parser.add_argument("password", type=str, default="")

    args = parser.parse_args()

    return args.webhook_url, args.host, args.port, args.user, args.password


def write_log_to_discord_by_log_type(log_type):
    current_log_filename = ftp_handler.get_current_log_filename_by_type(log_type=log_type)
    ftp_handler.save_current_log_by_type(current_log_filename=current_log_filename)
    messages = log_reader.get_messages_for_discord_by_type(log_type=log_type, current_log_filename=current_log_filename)

    discord_handler.send_messages_by_type(log_type=log_type, messages=messages)

def read_logs(scheduler): 
    print('Reading logs...')
    scheduler.enter(60, 1, read_logs, (scheduler,))
    
    write_log_to_discord_by_log_type(log_type=LOG_TYPE_ADMIN)

def main():
    ftp_handler.connect_and_login()
    ftp_handler.set_current_directory_to_log_directory()

    #log_read_scheduler.enter(60, 1, read_logs, (log_read_scheduler,))
    #log_read_scheduler.run()

    write_log_to_discord_by_log_type(log_type=LOG_TYPE_ADMIN)

if __name__ == "__main__":
    # TODO reuse above variables instead of hardcoded values
    #webhook_url, host, port, user, password = get_command_line_arguments();

    log_reader = LogReader()
    discord_handler = DiscordHandler(webhook_url="https://discord.com/api/webhooks/1119925532792995861/W5wdjKypB1mrLvs7_g6DXkNbrspkpAnxhzS1mVApx7N3g0M-tqv5bH0ijaTh2DVXNYzH")
    log_read_scheduler = sched.scheduler(time.time, time.sleep)
    ftp_handler = FTPHandler(host="176.57.173.175", port=51021, user="gpftp29875511127426533", password="F2uxTSmE")

    main()