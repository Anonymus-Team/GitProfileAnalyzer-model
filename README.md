# GitProfileAnalyzer-model

Модель классификации кода, на основе модели семейства [BERT](https://tfhub.dev/google/collections/transformer_encoders_text/1)

Обращение к модели происходит через микросервис.


### Preparing

### Install python dependencies

    pip install -r ./requirements.txt
    
    chmod +x ./analyze.sh

### usage
    
Linux:

    $ python3 ./grpc_server.py
