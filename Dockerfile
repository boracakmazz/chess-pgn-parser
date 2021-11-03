FROM python:3.10.0
ADD . /chess-educatioon-pgn-parser
WORKDIR /chess-educatioon-pgn-parser
RUN pip install -r requirements.txt