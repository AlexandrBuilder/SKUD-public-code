from flask_wtf import FlaskForm


class AppForm(FlaskForm):
    def full(self, object):
        for field in self:
            name = field.name
            if hasattr(object, name):
                field.default = getattr(object, name)
        self.process()
