FROM python:3.13-slim

COPY pyproject.toml .

RUN pip install uv && uv sync

COPY . .

CMD [ "sh", "-c", "python manage.py migrate && python manage.py collectstatic && gunicorn _project_.wsgi:application --host 0.0.0.0 --port 8000" ]
