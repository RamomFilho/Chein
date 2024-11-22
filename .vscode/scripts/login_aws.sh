#!/bin/bash


# Limpando JSON
# sed -e '/^\s*\/\//d' -e '/^ *\}/{H;x;s/\([^}]\),\n/\1\n/;b};x;/^ *}/d' .vscode/launch.json

json_launch=$(sed -e '/^\s*\/\//d' .vscode/launch.json) # Remove Comentários

# Lendo JSON
AWS_PROFILE=$(echo "$json_launch" | jq -r ".configurations[0].env.AWS_PROFILE")

# Execute the command and capture the output and error message
echo Executando no perfil AWS "$AWS_PROFILE"
output=$(aws configure export-credentials --profile $AWS_PROFILE --format env-no-export 2>&1)


# Check if the error message contains "Error when retrieving"
if echo "$output" | grep -q "Error"; then
  echo "Error detected. Executing aws sso login..."
  echo "$output"
  aws sso login --profile $AWS_PROFILE
  # aws configure export-credentials --profile "$AWS_PROFILE" --format env-no-export > .env
else
  # aws configure export-credentials --profile "$AWS_PROFILE" --format env-no-export > .env
  echo "Command executed successfully."
fi