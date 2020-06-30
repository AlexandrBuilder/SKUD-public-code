from app import db


def register(app):
    @app.cli.group()
    def database():
        """Database custom commands."""
        pass

    @database.command()
    def drop():
        """Drop database."""
        db.drop_all()
