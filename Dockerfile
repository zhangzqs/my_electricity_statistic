FROM python:3.10
COPY . /workspace
WORKDIR /workspace
ENTRYPOINT ["python"]
RUN pip install -r requirements.txt
CMD ["python", "main.py"]