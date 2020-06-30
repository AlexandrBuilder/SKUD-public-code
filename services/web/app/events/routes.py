from flask import request, redirect, url_for, render_template, flash, current_app

from app import db
from app.auth.decorators import role_required
from app.events import bp
from app.events.forms import SearchDateTimeForm, EventsForm
from app.models import Event, Role


@bp.route('/events', methods=['GET'])
@role_required([Role.ROLE_ADMIN, Role.ROLE_SECRETARY])
def events():
    page = request.args.get('page', 1, type=int)
    form = SearchDateTimeForm()
    events = Event.query
    if form.datetime_from.data is not None:
        events = events.filter(Event.timestamp >= form.datetime_from.data)
    if form.datetime_to.data is not None:
        events = events.filter(Event.timestamp <= form.datetime_to.data)
    events = events.order_by(Event.id).paginate(page, current_app.config['EVENTS_PER_PAGE'], False)
    return render_template('event/events.html', events=events, form=form)


@bp.route('/event/add', methods=['GET', 'POST'])
@role_required([Role.ROLE_ADMIN])
def event_add():
    form = EventsForm()
    if form.validate_on_submit():
        event = Event(
            type=form.type.data,
            timestamp=form.timestamp.data,
            user=form.user.data,
            link=form.link.data,
        )
        db.session.add(event)
        db.session.commit()
        flash('События добавлено', current_app.config['SUCCESS_FLASH'])
        return redirect(url_for('events.events'))
    return render_template('event/event_add.html', form=form)


@bp.route('/event/<int:id>/edit', methods=['GET', 'POST'])
@role_required([Role.ROLE_ADMIN])
def event_edit(id):
    event = Event.query.get_or_404(id)
    form = EventsForm(True)
    if request.method == 'GET':
        form.full(event)
    if form.validate_on_submit():
        event.type = form.type.data
        event.timestamp = form.timestamp.data
        event.user = form.user.data
        event.link = form.link.data
        db.session.commit()
        flash('Событие изменено', current_app.config['SUCCESS_FLASH'])
    return render_template('event/event_edit.html', form=form)


@bp.route('/event/<int:id>/delete', methods=['GET'])
@role_required([Role.ROLE_ADMIN])
def event_delete(id):
    event = Event.query.get_or_404(id)
    db.session.delete(event)
    db.session.commit()
    flash('Событие {} удалено'.format(id), current_app.config['SUCCESS_FLASH'])
    return redirect(url_for('events.events'))


@bp.route('/event/<int:id>', methods=['GET'])
@role_required([Role.ROLE_ADMIN, Role.ROLE_SECRETARY])
def event_view(id):
    event = Event.query.get_or_404(id)
    return render_template('event/event_view.html', event=event)
