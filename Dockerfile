FROM ubuntu:15.10
MAINTAINER "Yoanis Gil <gil.yoanis@gmail.com>"

RUN mkdir /srv/app

ENV WORKDIR=/srv/app
ENV VIRTUALENV_NAME=env

WORKDIR $WORKDIR

# Install require software and libraries
RUN apt-get -y update && \
    apt-get -y install python2.7 python-pip python-dev git vim nginx supervisor && \
    apt-get  clean && \
    rm -rf /var/lib/apt/lists/* && \
    pip install virtualenv==13.1.2 virtualenvwrapper==4.7.1 && \
    rm -rf ~/.pip/cache

RUN mkdir -p /etc/supervisord/conf.d

COPY ./docker/conf.d /etc/nginx/conf.d
COPY ./docker/nginx.conf /etc/nginx/nginx.conf
COPY ./docker/supervisord.conf /etc/supervisord/supervisord.conf
COPY ./docker/bin/gunicorn_start.sh /usr/local/bin/gunicorn_start.sh

# Add setup.sh so child images can build their environment.
ENV WORKON_HOME=/srv/app/.virtualenvs
COPY ./docker/bin/setup-virtualenv.sh /usr/local/bin/setup-virtualenv.sh

# Add a helper script to wrap activation of virtualenv
COPY ./docker/bin/wrap-virtualenv.sh /usr/local/bin/wrap-virtualenv.sh
COPY ./requirements.txt /srv/app/requirements.txt
RUN /usr/local/bin/setup-virtualenv.sh
COPY . /srv/app

RUN mkdir -p /var/lib/countdown && chown -R www-data: /var/lib/countdown

# Expose port 80
EXPOSE 80

# Application entrypoint
CMD ["supervisord", "-n", "-c", "/etc/supervisord/supervisord.conf"]
