'''
def mailer(sender, password_file, recipient, subject, body_text, \
            body_html, attachments):
'''
def mailer(sender, recipient, subject, body_text, \
            body_html, *attachments):
    print("attachments", attachments)
    import email,smtplib, ssl, os
    from email import encoders
    from email.mime.base import MIMEBase
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    os.system("cls")
    print("Mailer running")
    sender_email = sender
    receiver_email = recipient
    '''
    with open(password_file, 'r') as reader:
        password = reader.read() '''
    password = "At8l*nt~"
    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = sender
    message["To"] = recipient

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(body_text, "plain")
    part2 = MIMEText(body_html, "html")
    message.attach(part1)
    message.attach(part2)
    if attachments:
        print("attachments", attachments)
        n=3
        for item in attachments:
            print("item", item)
            # Open PDF file in binary mode
            with open(item, "rb") as attachment:
                print(attachment)

        # Add file as application/octet-stream
        # Email client can usually download this automatically as attachment
                part_number = "part" + str(n)
                part_number = MIMEBase("application", "octet-stream")
                part_number.set_payload(attachment.read())
                # Encode file in ASCII characters to send by email
                encoders.encode_base64(part_number)
                # Add header as key/value pair to attachment part
                part_number.add_header( "Content-Disposition", f"attachment; filename= {item}")
                message.attach(part_number)
                n += 1
    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first


    #print(message.as_string())
    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP('smtp-mail.outlook.com', 587) as server:
        server.ehlo()
        server.starttls()
        server.login(sender, password)
        server.sendmail('dardron@buckspgl.org','derrick.ardron@outlook.com', message.as_string())
    #server.quit()

def main():
    with open('c:\\pyproj\\contacts\\Contacts Email Text.TXT', 'r') as reader:
        body_text = reader.read()
    with open('c:\\pyproj\\contacts\\Contacts Email Text-2.HTML', 'r') \
            as reader:
        body_html = reader.read()
    mailer("dardron@buckspgl.org", "derrick.ardron@outlook.com", 'Lxxxx Provincial Email Failures - self test', body_text, body_html, "c:\\pyproj\\contacts\\Bucks PGL Survey v04.pdf", "c:\\pyproj\\contacts\\temp.csv")
    '''
    mailer("dardron@buckspgl.org", "c:\\pyproj\\password-dardron.txt", "derrick.ardron@outlook.com", 'Lxxxx Provincial Email Failures', body_text, body_html, ["c:\\pyproj\\contacts\\Bucks PGL Survey v04.pdf", "c:\\pyproj\\contacts\\temp.csv"])
    '''


if __name__ == '__main__':
    main()
