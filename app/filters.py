# -*- coding: utf-8 -*


def format_datetime(value):
    return value.strftime('%Y-%m-%d %H:%M')


def set_jinja_filters(app):
    app.jinja_env.filters['datetime'] = format_datetime


if __name__ == "__main__":
    pass
