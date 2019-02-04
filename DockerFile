FROM amsterdam/python

RUN rm -rf /data
RUN mkdir /data

COPY . /app/

WORKDIR /app/

RUN pip install -e .

CMD download_all_resources_from_dcatd_to_csv data catalog

