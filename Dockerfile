FROM python:3.12-alpine AS builder
WORKDIR /shorts
ENV PYTHONUNBUFFERED=1
RUN python3 -m pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install --no-cache-dir gunicorn
RUN pip install --no-cache-dir -r requirements.txt
COPY ./shorts .
RUN mkdir ./logs
RUN python3 manage.py collectstatic --noinput
COPY ./entrypoint.sh .
RUN chmod +x ./entrypoint.sh
ENTRYPOINT ["sh", "./entrypoint.sh"]

FROM nginx AS proxy
COPY ./https /etc/nginx/ssl
RUN cd /var && mkdir www
COPY ./favicon.ico /var/www
COPY --from=builder /shorts/staticfiles /var/www/static
COPY ./nginx.conf /etc/nginx/