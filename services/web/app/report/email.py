from flask import current_app
from app.email import send_email


def send_report(datetime_from, datetime_to, user, emails, attachments):
    if not user:
        message = 'Отчет на ({0} - {1}). В прикрепленном файле содержится информация о всех события происходящих в ' \
                  'промежутке от {0} до {1}'.format(datetime_from.strftime('%d/%m/%Y %H:%M:%S'),
                                                    datetime_to.strftime('%d/%m/%Y %H:%M:%S'))
        subject = 'Отчет на ({0} - {1}) об событиях огранизации'.format(datetime_from.strftime('%d/%m/%Y %H:%M:%S'),
                                                                        datetime_from.strftime('%d/%m/%Y %H:%M:%S'))
    else:
        message = 'Отчет на ({0} - {1}). В прикрепленном файле содержится информация о действиях пользователя "{2}" ' \
                  'происходящих в промежутке от {0} до {1}'.format(datetime_from.strftime('%d/%m/%Y %H:%M:%S'),
                                                      datetime_to.strftime('%d/%m/%Y %H:%M:%S'), str(user))
        subject = 'Отчет на ({0} - {1}) об пользователе {2}'.format(datetime_from.strftime('%d/%m/%Y %H:%M:%S'),
                                                                    datetime_to.strftime('%d/%m/%Y %H:%M:%S'),
                                                                    str(user))
    send_email(subject, current_app.config['MAIL_USERNAME'], emails, message, attachments)
