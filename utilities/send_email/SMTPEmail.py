import os
from os.path import basename

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.utils import formatdate

import smtplib
import ConfigParser


class EmailSender:
    @staticmethod
    def read_configure(section, option):
        try:
            script_dir = os.path.dirname(os.path.realpath(__file__))
            configure_file_path = os.path.join(script_dir, "configure")
            config = ConfigParser.ConfigParser()
            config.readfp(open(configure_file_path))
            return config.get(section, option)
        except Exception as error:
            print (error)
            raise

    @staticmethod
    def send(to_address, cc_address, subject, message, attaches):
        # Get configuration for server and admin email from configure file
        try:
            server_address = EmailSender.read_configure("smtp", "server")
            server_port = EmailSender.read_configure("smtp", "port")
            user = EmailSender.read_configure("smtp", "user")
            password = EmailSender.read_configure("smtp", "password")
        except Exception as error:
            print(error)
            return

        # Prepare email content to send
        email_package = MIMEMultipart()
        email_package["From"] = user
        email_package["To"] = to_address
        email_package["Cc"] = cc_address
        email_package["Subject"] = subject
        email_package["Date"] = formatdate(localtime=True)
        email_package.attach(MIMEText(message, 'plain', 'utf-8'))
        try:
            for attach in attaches:
                with open(attach, "rb") as fil:
                    part = MIMEApplication(fil.read(), Name=basename(attach))
                    part['Content-Disposition'] = 'attachment; filename="%s"' % basename(attach)
                    email_package.attach(part)
        except Exception as error:
            print (error)
            return

        # Access to mail server and send email
        try:
            server = smtplib.SMTP(server_address, server_port)
            server.ehlo()
            try:
                server.starttls()
            except Exception as error:
                print ("Warning: %s" % error)
            server.ehlo()
            try:
                server.login(user, password)
            except Exception as error:
                print ("Warning: %s" % error)
            server.sendmail(user, [to_address, cc_address], email_package.as_string())
            server.quit()
        except Exception as exception:
            print (exception)
            return