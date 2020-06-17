FROM python:3.7

WORKDIR /home

# django docker environment
RUN apt-get update
COPY requirements.txt /home/requirements.txt
RUN pip install -r requirements.txt
RUN git clone https://github.com/arteria/django-background-tasks.git \
    && cd django-background-tasks && pip install -r requirements.txt && python setup.py install

# node docker environment
RUN rm /bin/sh && ln -s /bin/bash /bin/sh
ENV NODE_VERSION 12.18.0
RUN curl -sL https://deb.nodesource.com/setup_12.x | bash -
RUN apt-get install -y aptitude nodejs
RUN npm install -g @vue/cli

RUN python -c "import nltk; nltk.download('brown'); nltk.download('stopwords'); nltk.download('punkt'); nltk.download('wordnet'); nltk.download('averaged_perceptron_tagger')"
RUN python -m spacy download en_core_web_sm

VOLUME ["/home"]
COPY . .

RUN npm install
RUN chmod +x /home/entrypoint.sh

EXPOSE 8080
EXPOSE 80
EXPOSE 8000
ENTRYPOINT [ "/home/entrypoint.sh" ]