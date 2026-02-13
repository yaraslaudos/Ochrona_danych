FROM python:3.11
WORKDIR /app
COPY requirements.txt .              
RUN pip install -r requirements.txt
COPY app/ .                        
EXPOSE 5000
CMD gunicorn --bind 0.0.0.0:5000 regestration:app