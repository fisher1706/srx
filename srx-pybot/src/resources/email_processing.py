import imaplib
import time
import re
import requests

class Email():
    def __init__(self, case):
        self.case = case
        self.email_address = case.activity.email_address
        self.email_password = case.activity.email_password
        self.imap = imaplib.IMAP4_SSL('imap.gmail.com', port=993)
        self.imap.login(self.email_address, self.email_password)

    def mark_all_emails_as_seen(self):
        self.imap.select('INBOX')
        status, response = self.imap.search(None, '(UNSEEN)')
        unread_msg_nums = list()
        unread_msg_nums = response[0].split()
        for e_id in unread_msg_nums:
            self.imap.store(e_id, '+FLAGS', '\Seen')

    def get_last_unseen_email_body(self, delay=180, email_from=None):
        emails_body = list()
        for second in range(1, delay):
            self.imap.select('INBOX')
            if (email_from is not None):
                status, response = self.imap.search(None, '(UNSEEN)', '(FROM "'+email_from+'")')
            else:
                status, response = self.imap.search(None, '(UNSEEN)')
            unread_msg_nums = list()
            unread_msg_nums = response[0].split()
            if (len(unread_msg_nums) == 0):
                if (second%10 == 0):
                    self.case.activity.logger.info(str(selay-second)+" seconds of awaiting left")
                time.sleep(1)
            else:
                for e_id in unread_msg_nums:
                    _, response = self.imap.fetch(e_id, '(UID BODY[TEXT])')
                    emails_body.append(response[0][1])
                break

        for e_id in unread_msg_nums:
            self.imap.store(e_id, '+FLAGS', '\Seen')

        if (len(emails_body) > 0):
            return emails_body[-1]
        else:
            return None

    def get_accept_invite_url_from_last_email(self):
        email_body = self.get_last_unseen_email_body(email_from="invite@storeroomlogix.com")
        url_template = self.case.activity.url.get_url_for_env("storeroomlogix.com/email/accept/", "auth")
        link = re.findall('href="('+url_template+'.*?)"', str(email_body))[-1]
        return link