FROM ubuntu:20.04
ARG DEBIAN_FRONTEND=noninteractive
RUN apt update
RUN apt install -y python3-pip python3-dev wget unzip
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt install -y ./google-chrome-stable_current_amd64.deb
RUN cd /usr/local/bin && ln -s /usr/bin/python3 python
RUN pip3 install selenium requests boto3 warrant pytest mail-parser beautifulsoup4 lxml pydantic pysftp
RUN cd /
RUN wget https://chromedriver.storage.googleapis.com/97.0.4692.71/chromedriver_linux64.zip
RUN unzip chromedriver_linux64.zip
RUN mv chromedriver /usr/local/bin
RUN wget -O "awscliv2.zip" "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip"
RUN unzip awscliv2.zip
RUN ./aws/install
