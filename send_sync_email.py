import boto3
from botocore.exceptions import ClientError
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time

from email_data import EMAILS


class EmailEngine:

    def __init__(self, emails):
        self.emails = emails

    def send_raw_email(self, sender, recipient, subject, body, tags, configuration_set):
        region_name = 'sa-east-1'
        SENDER = sender
        RECIPIENT = recipient
        CONFIGURATION_SET = configuration_set
        SUBJECT = subject
        BODY_TEXT = body
        BODY_HTML = body
        CHARSET = "utf-8"
        client = boto3.client('ses', region_name=region_name)
        msg = MIMEMultipart('mixed')
        msg['Subject'] = SUBJECT
        msg['From'] = SENDER
        msg['To'] = RECIPIENT
        msg['Reply-To'] = SENDER
        msg_body = MIMEMultipart('alternative')
        textpart = MIMEText(BODY_TEXT.encode(CHARSET), 'plain', CHARSET)
        htmlpart = MIMEText(BODY_HTML.encode(CHARSET), 'html', CHARSET)
        msg_body.attach(textpart)
        msg_body.attach(htmlpart)
        msg.attach(msg_body)
        msg.add_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        msg.add_header('Cache - Control', 'post - check = 0, pre - check = 0')
        msg.add_header('Pragma', 'no-cache')
        try:
            # Provide the contents of the email.
            response = client.send_raw_email(
                Source=SENDER,
                Destinations=[
                    RECIPIENT
                ],
                RawMessage={
                    'Data': msg.as_string(),
                },
                ConfigurationSetName=CONFIGURATION_SET,
                Tags=tags
            )
        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            print(subject)

    def run(self):
        for _email in self.emails:
            self.send_raw_email(**_email)


if __name__ == '__main__':
    start_time = time.time()
    runner = EmailEngine(emails=EMAILS)
    runner.run()
    end_time = time.time()
    print("--- %s seconds ---" % (end_time - start_time))
