FROM python
WORKDIR /app
COPY geometric_lib/ ./geometric_lib/
COPY script.py .
RUN chmod +x script.py
VOLUME ["/config"]
CMD python script.py