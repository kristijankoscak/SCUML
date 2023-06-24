from datetime import datetime
from handlers.log_reader import LOG_TYPE_ADMIN
from discord_webhook import DiscordWebhook, DiscordEmbed


class DiscordHandler:
    def __init__(self, webhook_url) -> None:
        self.webhook_url = webhook_url        


    def extract_data_from_admin_log(self, line): 
        line_parts = line.split('\'', 2)

        date_time = line_parts[0].replace(':', '')
        user = line_parts[1].replace('\'', '')
        command = line_parts[2].replace('\'', '')

        return date_time, user, command

    def send_message(self, embed):
        webhook = DiscordWebhook(url=self.webhook_url)
        
        webhook.add_embed(embed=embed)
        webhook.execute()

    
    def send_admin_message(self, message):
        today = datetime.utcnow().strftime('%Y-%m-%d %H:%M')
        _, user, command = self.extract_data_from_admin_log(message)
        admin_embed = DiscordEmbed(
            title=user, 
            description=command,
            author=dict(
                name= "🅰dministrator"
            ),
            color="FF0000",
            timestamp=today)
        
        self.send_message(embed=admin_embed)

    def send_messages_by_type(self, log_type, messages):
        for message in messages:
            if log_type == LOG_TYPE_ADMIN:
                self.send_admin_message(message=message)

