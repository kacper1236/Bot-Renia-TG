# Gwarantujemy, że zawsze wystartujemy z tym obrazem. Dzięki temu wszystko
# powinno być powtarzalne.
FROM python:3.9-alpine@sha256:756e9fe7f6ad5a18d302006b445d3c9e8e1d868938c2562415a30c240e4bdd56

# Kopiujemy requirements.txt w tym moment, ponieważ jest istotny tylko dla
# następującej po nim warstwy. Brak zmian w tym pliku nie wywoła ponownego
# przejścia następującej warstwy RUN.
#COPY requirements.txt /tmp/requirements.txt
COPY requirements.frozen.txt /tmp/requirements.txt
RUN apk add --no-cache postgresql-libs && \
    apk add --no-cache --virtual .build-deps musl-dev postgresql-dev && \
    python3 -m pip install --prefer-binary --no-cache-dir -r /tmp/requirements.txt --no-cache-dir && \
    rm /tmp/requirements.txt && \
    apk --purge del .build-deps postgresql-dev musl-dev

EXPOSE 5001
# W ten sposób entrypoint będzie krótszy, a przy okazji zachowamy zgodność ze
# standardem FHS: https://refspecs.linuxfoundation.org/FHS_3.0/fhs/index.html
# Ale żeby to miało prawo działać, app.py musi mieć shebang oraz bit +x.
COPY app.py /usr/local/bin/renia-backend
ENTRYPOINT ["renia-backend"]
