FROM python:3.7

WORKDIR /home

# django docker environment
RUN apt-get update
COPY requirements.txt /home/requirements.txt
RUN pip install -r requirements.txt
RUN git clone https://github.com/arteria/django-background-tasks.git \
    && cd django-background-tasks && pip install -r requirements.txt && python setup.py install
RUN python -c "import nltk; nltk.download('brown'); nltk.download('stopwords')"

# node docker environment
RUN rm /bin/sh && ln -s /bin/bash /bin/sh
ENV NODE_VERSION 12.18.0
RUN curl -sL https://deb.nodesource.com/setup_12.x | bash -
RUN apt-get install -y aptitude nodejs
RUN npm install -g @vue/cli

VOLUME ["/home"]
COPY . .
RUN chmod +x /home/entrypoint.sh
EXPOSE 8080
EXPOSE 80
ENTRYPOINT [ "/home/entrypoint.sh" ]