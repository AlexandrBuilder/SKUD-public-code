from datetime import datetime

from flask import render_template, flash, current_app, send_file

from app.auth.decorators import role_required
from app.models import User, Role
from app.report import bp
from app.report.documents import get_report_file
from app.report.email import send_report
from app.report.forms import ReportForm


@bp.route('/report', methods=['GET', 'POST'])
@role_required([Role.ROLE_ADMIN, Role.ROLE_SECRETARY])
def report():
    form = ReportForm()
    if form.validate_on_submit():
        user = None
        if form.type.data == ReportForm.TYPE_BY_EMPLOYER:
            user = form.user.data
        file = get_report_file(form.datetime_from.data, form.datetime_to.data, user)
        file_title = 'report_{}.xls'.format(datetime.now().strftime("%d/%m/%Y_%H:%M:%S"))
        if not file:
            if user:
                flash('Нету событий по пользователю "{}" за этот промежуток веремени'.format(user),
                      current_app.config['ERROR_FLASH'])
            else:
                flash('Нету событий за этот промежуток веремени', current_app.config['ERROR_FLASH'])
        elif form.submit_email.data:
            emails = [user.email for user in User.query.filter_by(send_flag=True).all()]
            if len(emails) == 0:
                flash('Отсутвуют получатели', current_app.config['ERROR_FLASH'])
            else:
                attachments = [(file_title, 'application/ms-excel', file.getvalue())]
                send_report(form.datetime_from.data, form.datetime_to.data, user, emails, attachments)
                flash('Email сообщения отпарвлены по следующим адресам: {}'.format(', '.join(emails)),
                      current_app.config['SUCCESS_FLASH'])
        elif form.submit_excel.data:
            return send_file(file, attachment_filename=file_title, as_attachment=True)
    return render_template('report/report.html', form=form)
