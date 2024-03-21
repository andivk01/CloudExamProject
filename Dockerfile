FROM locustio/locust

RUN pip install xmltodict

CMD ["locust"]