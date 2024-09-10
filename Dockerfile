FROM python:2.7
MAINTAINER Pinegap.io "support@pinegap.io"
LABEL Name="Pinegap Manager" Version="2.1"

ENV PYTHONUNBUFFERED 1
RUN mkdir -p /opt/pinegap-manager/
WORKDIR /opt/pinegap-manager/
COPY . /opt/pinegap-manager/
COPY app/settings.py.sample /opt/pinegap-manager/app/settings.py

RUN apt-get update -yq
RUN apt-get install -yq --no-install-recommends virtualenv python-pip libmagic-dev
RUN apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
	&& rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN virtualenv env
RUN /bin/bash -c "source env/bin/activate && pip install -r requirements.txt && deactivate"


EXPOSE 8003
ENTRYPOINT ["/opt/pinegap-manager/docker-entrypoint.sh"]
CMD ["run"]
