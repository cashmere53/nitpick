FROM python:3.10.6-slim-bullseye

RUN apt update && \
    apt upgrade -y  &&\
    apt install -y git

RUN pip install --upgrade pip

RUN adduser melon
ENV HOME /home/melon
WORKDIR ${HOME}
USER melon

COPY . .
RUN python -m pip install .

EXPOSE 443

CMD [ "python", "-m", "nitpick" ]
