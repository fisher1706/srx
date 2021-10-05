FROM ubuntu:20.04
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update
RUN apt-get install -y python3-pip python3-dev wget google-chrome-stable unzip
RUN cd /usr/local/bin && ln -s /usr/bin/python3 python
RUN pip3 install selenium requests boto3 warrant pytest mail-parser beautifulsoup4 lxml
RUN cd /
RUN wget https://chromedriver.storage.googleapis.com/94.0.4606.61/chromedriver_linux64.zip
RUN unzip chromedriver_linux64.zip
RUN mv chromedriver /usr/local/bin
RUN wget -O "awscliv2.zip" "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip"
RUN unzip awscliv2.zip
RUN ./aws/install
