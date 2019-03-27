FROM hseling/hseling-api-base:python3.6-alpine3.7 as build

LABEL maintainer="Sergey Sobko <ssobko@hse.ru>"

RUN mkdir /dependencies
COPY ./requirements.txt /dependencies/requirements.txt
COPY ./setup.py /dependencies/setup.py

RUN pip install -r /dependencies/requirements.txt

FROM hseling/hseling-api-base:python3.6-alpine3.7 as production

COPY --from=build /usr/local/lib/python3.6/site-packages /usr/local/lib/python3.6/site-packages
COPY --from=build /usr/lib/python3.6/site-packages /usr/lib/python3.6/site-packages

COPY --from=build /dependencies /dependencies

VOLUME ./data
COPY ./antislovari.sql /docker-entrypoint-initdb.d/antislovari.sql

COPY ./hseling_api_anti_slovari /dependencies/hseling_api_anti_slovari
RUN pip install /dependencies

COPY ./app /app
