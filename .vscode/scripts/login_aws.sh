#!/bin/bash

# Executa o comando e captura a saida da mensagem
output=$(aws configure export-credentials --profile Ramom --format env-no-export 2>&1)

# Verifica se contem Error na mensagem retornada
if echo "$output" | grep -q "Error"; then
  echo "Error detectado. Executando aws sso login..."
  aws sso login --profile Ramom
  aws configure export-credentials --profile Ramom --format env-no-export > .env
else
  aws configure export-credentials --profile Ramom --format env-no-export > .env
  echo "Comando Executado com Sucesso!"
fi