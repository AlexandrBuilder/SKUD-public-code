from app.forms import AppForm
from app.models import User, Event
from wtforms import SubmitField, SelectField, DateTimeField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired


class ReportForm(AppForm):
    TYPE_BY_ORGANIZATION = 'TYPE_BY_ORGANIZATION'
    TYPE_BY_EMPLOYER = 'TYPE_BY_EMPLOYER'

    datetime_from = DateTimeField('От', format='%Y-%m-%dT%H:%M:%S',
                                  validators=[DataRequired(message='Поле не должно быть пустым')])
    datetime_to = DateTimeField('До', format='%Y-%m-%dT%H:%M:%S',
                                validators=[DataRequired(message='Поле не должно быть пустым')])
    type = SelectField("Тип отчета", choices=[
        ('TYPE_BY_ORGANIZATION', 'По организации'),
        ('TYPE_BY_EMPLOYER', 'По сотруднику')
    ])
    user = QuerySelectField(
        'Пользователь',
        query_factory=lambda: User.query,
        allow_blank=False,
        get_pk=lambda a: a.id
    )

    def __init__(self, *args, **kwargs):
        super(ReportForm, self).__init__(*args, **kwargs)
        first_event = Event.query.first()
        last_event = Event.query.order_by(Event.id.desc()).first()

        if first_event and self.datetime_from.data is None:
            self.datetime_from.data = first_event.timestamp
        if last_event and self.datetime_to.data is None:
            self.datetime_to.data = last_event.timestamp

    submit_email = SubmitField('Разослать отчеты по Email')
    submit_excel = SubmitField('Получить отчет в формате Excel')
