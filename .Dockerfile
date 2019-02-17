# Use the newest version of python
FROM python:latest

# Copy contents from this directory over into the volume inside the container
WORKDIR . /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./your-daemon-or-script.py" ]


# To build and run the image and container
# docker build -t Drowsy_Driver .
# docker run -it --rm --name Drowsy_Driver_app Drowsy_Driver