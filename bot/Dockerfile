FROM python:3.9-slim@sha256:5fa679d492e5cb06ce42ddbfb02609291f80f3288b799f6bc2b752a8b51268fc

#COPY requirements.txt /tmp/requirements.txt
COPY requirements.frozen.txt /tmp/requirements.txt
RUN python3 -m pip install --prefer-binary --no-cache-dir -r /tmp/requirements.txt && \
    rm /tmp/requirements.txt

COPY src /usr/local/lib/python3.9/renia_bot

COPY main.py /usr/local/bin/renia-bot
VOLUME /var/log/renia
VOLUME /var/lib/photos
ENTRYPOINT ["renia-bot"]
