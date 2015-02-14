'''Sloth CI extension that adds an SMTP handler to the build logger in Sloth CI apps.

.. warning::

    This extension uses the default Python SMTPHandler from logging.handlers. SMTPHandler doesn't work with GMail's SMTP because it creates an smtplib.SMTP object to connect to the host, whereas GMail requires smtplib.SMTP_SSL.

    Outlook.com is approved to work fine.

Extension params::
    
    # Use the module sloth-ci.ext.build_email_notifications.
    module: build_email_notifications

    # Emails to send the notifications to.
    emails:
        - foo@bar.com
        - admin@example.com
    
    # Log level (number or valid Python logging level name).
    # ERROR includes only build fails, WARNING adds partial completions,
    # INFO adds completion, and DEBUG adds trigger notifications.
    # Default is WARNING.
    level: INFO

    # The "from" address in the emails. Default is "build@sloth.ci."
    from: notify@example.com

    # The email subject on build trigger. You can use the {listen_point} placeholder.
    # Default is "{listen_point}: Build Triggered."
    subject_triggered: 'Triggered build on {listen_point}!'

    # The email subject on build completion.You can use the {listen_point} placeholder.
    # Default is "{listen_point}: Build Completed."
    subject_completed: 'Hooray! {listen_point} works!'

    # The email subject on build partial completion. You can use the {listen_point} placeholder.
    # Default is "{listen_point}: Build Partially Completed."
    subject_partially_completed: 'Better than nothing on {listen_point}'

    # The email subject on build fail. You can use the {listen_point} placeholder.
    # Default is "{listen_point}: Build Failed."
    subject_failed: 'Fail on {listen_point}'

    # SMTP settings.
    # SMTP mail host and (if not default) port.
    # Mandatory parameter.
    mailhost: 'smtp-mail.outlook.com:25'
    
    # SMTP login.
    login: foo@bar.baz

    # SMTP password.
    password: bar

    # If the SMTP server requires TLS, set this to true. Default is false.
    # If necessary, you can provide a keyfile name or a keyfile and a certificate file names.
    # This param is used only the login and password params are supplied.
    secure: true
    # secure:
    #    -   keyfile
    #    -   cerfile
'''


__title__ = 'sloth-ci.ext.build_email_notifications'
__description__ = 'Build email notifications for Sloth CI apps'
__version__ = '1.0.4'
__author__ = 'Konstantin Molchanov'
__author_email__ = 'moigagoo@live.com'
__license__ = 'MIT'


def extend(cls, extension):
    import logging
    from logging.handlers import SMTPHandler


    class Sloth(cls):
        def __init__(self, config):
            super().__init__(config)
            
            build_email_config = extension['config']
            
            split_mail_host = build_email_config['mail_host'].split(':')

            if len(split_mail_host) == 2:
                mail_host = (split_mail_host[0], split_mail_host[1])
            
            else:
                mail_host = split_mail_host[0]
            
            from_addr = build_email_config.get('from', 'build@sloth.ci')

            to_addrs = build_email_config.get('emails', [])

            smtp_login = build_email_config.get('login')

            if smtp_login:
                credentials = (smtp_login, build_email_config['password'])
            
            else:
                credentials = None

            secure = build_email_config.get('secure')

            if secure == True:
                secure = ()

            elif secure:
                secure = tuple(secure)

            else:
                secure = None

            self._subjects = {
                'triggered': build_email_config.get('subject_triggered', '{listen_point}: Build Triggered'),
                'completed': build_email_config.get('subject_completed', '{listen_point}: Build Completed'),
                'partially_completed': build_email_config.get('subject_partially_completed', '{listen_point}: Build Partially Completed'),
                'failed': build_email_config.get('subject_failed', '{listen_point}: Build Failed')
            }
            
            smtp_handler = SMTPHandler(
                mailhost=mail_host,
                fromaddr=from_addr,
                toaddrs=to_addrs,
                subject='Sloth CI: Build Notification',
                credentials=credentials,
                secure=secure
            )

            smtp_handler.getSubject = self._get_email_subject
            
            smtp_handler.setLevel(build_email_config.get('level', logging.WARNING))
            
            self.build_logger.addHandler(smtp_handler)

            self.log_handlers[extension['name']] = smtp_handler

        def stop(self):
            super().stop()
            self.build_logger.removeHandler(self.log_handlers.pop(extension['name']))

        def _get_email_subject(self, record):
            '''Get a subject based on record level.'''

            if record.levelname == 'INFO':
                if 'Triggered' in record.getMessage():
                    return self._subjects['triggered'].format(listen_point=self.listen_point)

                else:
                    return self._subjects['completed'].format(listen_point=self.listen_point)
        
            elif record.levelname == 'WARNING':
                return self._subjects['partially_completed'].format(listen_point=self.listen_point)

            elif record.levelname == 'ERROR':
                return self._subjects['failed'].format(listen_point=self.listen_point)


    return Sloth
