FROM continuumio/anaconda3

RUN conda update -y -n base conda
RUN conda install -c ioam datashader xarray holoviews bokeh

RUN apt install -y libgl1-mesa-glx

COPY LICENSE ./LICENSE
COPY README.md ./README.md
COPY ./main.py /yape2/main.py
COPY ./scripts/* /yape2/scripts/

EXPOSE 5006

ENTRYPOINT ["bokeh", "serve","/yape2", "--args"]
