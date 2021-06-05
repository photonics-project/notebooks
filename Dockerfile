FROM python:3.8-slim

RUN apt update && apt install -y \
    gfortran \
    make

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY ./requirements/ /notebooks/requirements/
RUN pip install --no-cache-dir -r /notebooks/requirements/requirements.txt

COPY ./ /notebooks/

WORKDIR /notebooks/
RUN make data --directory=./lowtran/
RUN make notebooks

EXPOSE 8866

ENTRYPOINT ["voila", "--port=8866", "--no-browser"]
