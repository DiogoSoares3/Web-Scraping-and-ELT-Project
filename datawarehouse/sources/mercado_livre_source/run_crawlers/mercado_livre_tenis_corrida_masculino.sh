#!/bin/bash

scrapy crawl mercado_livre_tenis_corrida_masculino -o data/mercado_livre_tenis_corrida_masculino.json

### Esse script so pode ser executado no diretório que contém o seu arquivo de configuração (scrapy.cfg).
### Talvez separar cada DAG para cada plataforma (mercado livre, amazon, etc), pois assim podemos escalonar a execução com base em plataforma.
### Para organizar os scripts bash que cada DAG vai executar, é melhor termos um arquivo scrapy.cfg para cada DAG, ou seja, para cada plataforma.

### SUGESTÃO: Posteriormente deixar esse comando que executa o scrapy no próprio BashOperator da DAG.