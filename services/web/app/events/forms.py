from app.forms import AppForm
from app.models import User, Event
from flask import request
from wtforms import SubmitField, SelectField, TextAreaField, DateTimeField
from wtforms.ext.sqlalchemy.fields import QuerySelectField


class SearchDateTimeForm(AppForm):
    datetime_from = DateTimeField('От', format='%Y-%m-%dT%H:%M:%S')
    datetime_to = DateTimeField('До', format='%Y-%m-%dT%H:%M:%S')
    submit = SubmitField('Искать')

    def __init__(self, *args, **kwargs):
        if 'formdata' not in kwargs:
            kwargs['formdata'] = request.args
        if 'csrf_enabled' not in kwargs:
            kwargs['csrf_enabled'] = False
        super(SearchDateTimeForm, self).__init__(*args, **kwargs)
        first_event = Event.query.order_by(Event.timestamp.asc()).first()
        last_event = Event.query.order_by(Event.timestamp.desc()).first()
        if first_event and self.datetime_from.data is None:
            self.datetime_from.data = first_event.timestamp
        if last_event and self.datetime_to.data is None:
            self.datetime_to.data = last_event.timestamp


class EventsForm(AppForm):
    type = SelectField('Событие', choices=Event.EVENTS)
    timestamp = DateTimeField('Время', format='%Y-%m-%dT%H:%M:%S')
    link = TextAreaField('Ссылка')
    user = QuerySelectField(
        'Пользователь',
        query_factory=lambda: User.query,
        allow_blank=True,
        get_pk=lambda a: a.id
    )
    submit = SubmitField('Добавить')

    def __init__(self, edit_form=False, *args, **kwargs):
        super(EventsForm, self).__init__(*args, **kwargs)
        if edit_form:
            self.submit.label.text = 'Изменить'
