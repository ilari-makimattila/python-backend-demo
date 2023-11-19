FROM python:3.11-slim

RUN pip install 'poetry>=1.2.0,<2.0'
RUN useradd -m python

ENV WORKDIR /app
WORKDIR ${WORKDIR}
RUN chown python:python /app

COPY docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]

USER python

COPY --chown=python:python . ${WORKDIR}
RUN poetry install --no-dev
