FROM python:3.6

COPY yape /yape/yape
COPY setup.py /yape/setup.py
WORKDIR /yape/
RUN pip install --upgrade pip
RUN cd /yape && pip install .

ENTRYPOINT ["yape"]
CMD [ "-h" ]
