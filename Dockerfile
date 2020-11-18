FROM python:3-alpine

RUN apk update && \
    apk upgrade && \
    apk --no-cache --update-cache add git gcc gfortran build-base wget freetype-dev libpng-dev openblas-dev jpeg-dev py-pip

RUN ln -s /usr/include/locale.h /usr/include/xlocale.h
RUN pip install --upgrade pip && \
    pip install --no-cache-dir Cython numpy pandas matplotlib pytz gitchangelog pre-commit black pystache bokeh PyYAML pillow setuptools_scm setuptools

RUN pip install --no-cache-dir -e git+https://github.com/murrayo/yape.git#egg=yape

ENTRYPOINT ["yape"]
CMD [ "-h" ]
