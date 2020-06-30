from app.documents import create_xls_file
from app.models import Event


def get_report_file(datetime_from, datetime_to, user=None):
    events = Event.query
    if datetime_from is not None:
        events = events.filter(Event.timestamp >= datetime_from)
    if datetime_to is not None:
        events = events.filter(Event.timestamp <= datetime_to)
    if user is not None:
        events = events.filter(Event.user.has(id=user.id))
    if events.count() <= 0:
        return None
    data_rows = [['ID', 'Пользователь', 'Дествие', 'Время', 'Ссылка']]
    data_keys = ['id', 'user', 'type', 'timestamp', 'link']
    for event in events.all():
        data_list = []
        for key in data_keys:
            if key == 'timestamp':
                data_list.append(
                    getattr(event, key).strftime('%d/%m/%Y %H:%M:%S')
                )
            elif key == 'user':
                data_list.append(
                    str(getattr(event, key))
                )
            else:
                data_list.append(getattr(event, key))
        data_rows.append(data_list)
    return create_xls_file(data_rows)
