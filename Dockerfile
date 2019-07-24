FROM python:3-alpine

RUN apk update && \
    apk upgrade && \
    apk --no-cache --update-cache add git gcc gfortran python python-dev py-pip build-base wget freetype-dev libpng-dev openblas-dev py-numpy py-scipy py-pillow jpeg-dev

RUN ln -s /usr/include/locale.h /usr/include/xlocale.h
RUN pip install --upgrade pip && \
    pip install --no-cache-dir pandas matplotlib

RUN pip install --no-cache-dir -e git+https://github.com/casep/yape.git#egg=yape

ENTRYPOINT ["yape"]
CMD [ "-h" ]

