FROM python:3.8
RUN apt-get install -y git
RUN mkdir /script
WORKDIR /script
RUN cp -r python-jinja2-login /script
WORKDIR /script/python-jinja2-login
RUN pip install -r requirements.txt
EXPOSE 4000
ENTRYPOINT [ "python" ]
CMD [ "app.py" ]
