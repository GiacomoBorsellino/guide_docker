1. Prerequisiti
   Assicurati di avere installato su WSL (Ubuntu):

✅ Python
bash

sudo apt update
sudo apt install python3 python3-pip

✅ Docker + Docker Compose
Se non li hai:

bash

sudo apt install docker.io docker-compose
sudo service docker start

Aggiungiti al gruppo docker per evitare sudo ogni volta:

bash

sudo usermod -aG docker $USER

# Poi esci e rientra nella sessione WSL

📁 2. Struttura del progetto
Dentro la tua cartella my-container-server, crea:

my-container-server/
├── app.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml

🐍 3. Codice Python (Flask)
🔹 app.py

python

from flask import Flask, jsonify
import psycopg2

app = Flask(**name**)

@app.route("/items")
def get_items():
conn = psycopg2.connect(
dbname="mydb",
user="giacomo",
password="giacomo_password",
host="db" # nome del servizio DB nel docker-compose
)
cur = conn.cursor()
cur.execute("SELECT id, name FROM items;")
items = cur.fetchall()
cur.close()
conn.close()
return jsonify([{"id": i[0], "name": i[1]} for i in items])

if "**name**" == "**main**":
app.run(host="0.0.0.0", port=3000)

📦 4. Dipendenze Python
🔹 requirements.txt

txt

flask
psycopg2-binary
🔸 Nota: usiamo psycopg2-binary perché è più facile da installare in Docker.

🐳 5. Dockerfile per il backend
🔹 Dockerfile

Dockerfile

FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python3", "app.py"]

⚙️ 6. Docker Compose per orchestrare tutto
🔹 docker-compose.yml

yaml

version: '3.8'

services:
db:
image: postgres:15
container_name: my-container-server-db-1
environment:
POSTGRES_DB: mydb
POSTGRES_USER: giacomo
POSTGRES_PASSWORD: giacomo_password
ports: - "5432:5432"
volumes: - pgdata:/var/lib/postgresql/data

web:
build: .
container_name: my-container-server-web-1
ports: - "3000:3000"
depends_on: - db

volumes:
pgdata:

🚀 7. Avvio del progetto

Da dentro la cartella:

bash

sudo docker-compose up --build
Vedrai il log del DB e di Flask. L'app sarà raggiungibile da: http://localhost:3000/items

🗃️ 8. Crea container e crea tabella nel DB

bash

sudo docker-compose up --build

Dettaglio:

- image: postgres:15 → Docker scarica l’immagine ufficiale di PostgreSQL versione 15 dal Docker Hub (se non è già presente localmente).
- container_name → dà un nome al container per poterlo riconoscere facilmente.
- environment → variabili d’ambiente per configurare il DB al primo avvio:
- POSTGRES_DB: nome del database creato all’avvio (mydb)
- POSTGRES_USER: utente con cui accedere (giacomo)
- POSTGRES_PASSWORD: password per l’utente (giacomo_password)
- ports → mappa la porta 5432 interna del container sulla porta 5432 della tua macchina, così puoi accedere al DB da fuori.
- volumes → monta un volume chiamato pgdata per persistere i dati anche se il container viene cancellato.

Apri una shell nel container PostgreSQL:

bash

sudo docker exec -it my-container-server_db_1 psql -U giacomo -d mydb

Dentro psql, crea la tabella items:

sql

CREATE TABLE items (
id SERIAL PRIMARY KEY,
name TEXT NOT NULL
);

Verifica che sia creata:

sql

\d items
📥 9. Inserire dati nel DB
🔹 Inserire 10.000 righe con valore "micheal primo is the best!"

sql

INSERT INTO items (name)
SELECT 'micheal primo is the best!'
FROM generate_series(1, 10000);

(Un inside joke :P)

Controlla:

sql

SELECT COUNT(\*) FROM items;

Verifica:

sql

SELECT COUNT(\*) FROM items WHERE name = 'micheal primo is the best!';

🔄 11. Test dell'API
Fuori da psql, prova:

bash

curl http://localhost:3000/items
Dovresti vedere una lista JSON dei record.

✅ Risultato
Hai:

- Un'app Flask in un container Docker
- Un DB PostgreSQL in un secondo container
- Comunicazione tra i due via Docker Compose
- API /items che legge dal database
- Inserito e aggiornato 10.000 record reali

📁 Rimuovere i containers

1. Come rimuovere tutto:

- sudo docker-compose down
- sudo docker volume rm my-container-server_pgdata
- sudo docker volume ls

2. Rimuovere le immagini (opzionale)
   Se vuoi liberare spazio o ricostruire da zero anche le immagini Docker:

Lista immagini:

bash

- sudo docker images
  Rimuovi immagine con:

bash

- sudo docker rmi nome_immagine
  Esempio per la tua immagine backend (se l’hai costruita localmente):

bash

- sudo docker rmi my-container-server-web-1

3. Pulizia avanzata (tutti i container, volumi e reti non usati)
   Se vuoi un cleanup totale, usa:

bash

- sudo docker system prune --volumes
