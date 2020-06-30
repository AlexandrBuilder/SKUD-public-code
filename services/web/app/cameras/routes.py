from app import db
from app.auth.decorators import role_required
from app.cameras import bp
from app.cameras.video_stream import VideoStream
from app.models import Camera, Role, Event
from flask import request, redirect, url_for, render_template, Response


@bp.route('/', methods=['GET'])
@bp.route('/main', methods=['GET'])
@role_required([Role.ROLE_ADMIN, Role.ROLE_SECRETARY])
def main():
    events = Event.query.order_by(Event.timestamp.desc()).limit(5).all()
    event = Event.query.order_by(Event.timestamp.desc()).first()
    cameras_dict = {i: Camera.query.filter_by(position=i).filter_by(context=Camera.CONTEXT_MAIN_PAGE).first() for i in
                    range(1, 3)}
    return render_template('camera/main.html', cameras=cameras_dict, events=events, event=event)


@bp.route('/last-events', methods=['GET'])
@role_required([Role.ROLE_ADMIN, Role.ROLE_SECRETARY])
def last_events():
    last_id = request.args.get("last_id", type=int)
    last_event = None
    if last_id:
        last_event = Event.query.get(last_id)
    events = Event.query.filter(Event.timestamp > last_event.timestamp) if last_event else Event.query
    event = Event.query.order_by(Event.timestamp.desc()).first()
    return render_template('camera/widgets/events-box.html', events=events.all(), event=event)


@bp.route('/cameras', methods=['GET', 'POST'])
@role_required([Role.ROLE_ADMIN, Role.ROLE_SECRETARY])
def cameras():
    cameras_dict = {i: Camera.query.filter_by(context=Camera.CONTEXT_CAMERAS).filter_by(position=i).first() for i in
                    range(1, 10)}
    return render_template('camera/camera.html', cameras=cameras_dict)


@bp.route('/camera/add/<string:context>', methods=['POST'])
@role_required([Role.ROLE_ADMIN, Role.ROLE_SECRETARY])
def add_camera(context):
    camera = Camera(link=request.form.get('link'), position=request.form.get('position'), context=context)
    db.session.add(camera)
    db.session.commit()
    url = url_for('cameras.cameras') if Camera.CONTEXT_CAMERAS == context else url_for('cameras.main')
    return redirect(url)


@bp.route('/camera/<int:id>/<string:context>', methods=['POST'])
@role_required([Role.ROLE_ADMIN, Role.ROLE_SECRETARY])
def edit_camera(id, context):
    camera = Camera.query.get_or_404(id)
    camera.link = request.form.get('link')
    db.session.commit()
    url = url_for('cameras.cameras') if Camera.CONTEXT_CAMERAS == context else url_for('cameras.main')
    return redirect(url)


@bp.route('/camera/<int:id>/delete/<string:context>', methods=['GET'])
@role_required([Role.ROLE_ADMIN, Role.ROLE_SECRETARY])
def delete_camera(id, context):
    camera = Camera.query.get_or_404(id)
    db.session.delete(camera)
    db.session.commit()
    url = url_for('cameras.cameras') if Camera.CONTEXT_CAMERAS == context else url_for('cameras.main')
    return redirect(url)


@bp.route('/camera/video_stream')
@role_required([Role.ROLE_ADMIN, Role.ROLE_SECRETARY])
def video_stream():
    stream = VideoStream(request.args.get('link'))
    return Response(stream.stream(), mimetype='multipart/x-mixed-replace; boundary=frame')
