FROM python:3.7.2



ENV APP_USER=mohamed
ENV APP_PATH=/app
RUN mkdir $APP_PATH
RUN useradd --system --shell /bin/true --home $APP_PATH $APP_USER


ADD requirements-dev.txt $APP_PATH/requirements.txt


RUN apt-get update && apt-get -y upgrade && \
    apt-get -y install build-essential && \
    python -m pip install -r $APP_PATH/requirements.txt && \
    rm -f $APP_PATH/requirements.txt && \
    apt-get -y remove build-essential && \
    chmod +x $APP_PATH/run.sh && \
    mkdir /creds && chown $APP_USER:$APP_USER /creds

ENV PYTHONPATH "${PYTHONPATH}:."

ADD bin /app/bin
ADD tests /app/tests
ADD lib /app/lib
ADD configurations/ /app/configurations
ADD config.py /app/config.py

USER $APP_USER
WORKDIR $APP_PATH

CMD [$APP_PATH/bin/run_drugs_relations_pipeline.py, "-flag"]