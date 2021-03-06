import mailer

from blog.mail.email_template import get_email_text

# WARNING! Disabling email is used only during development process! ALWAYS TURN EMAIL ON BEFORE DEPLOYMENT!
EMAIL_ENABLED = True
SMTP_ADDRESS = 'mail.inet.fi'
SMTP_PORT = 25


def send_mail(address, username, link, template):
    if EMAIL_ENABLED:
        message = mailer.Message(From="noreply@mstefan99.com", To=address)
        message.Subject, message.Html = get_email_text(username, link, template)

        sender = mailer.Mailer(SMTP_ADDRESS, SMTP_PORT)
        sender.send(message)
