#!/bin/bash

# Da eseguire nella stessa directory dove si trova id_rsa

> ocp-info.out

# Crea list con hostname e relativo IP
oc get node -o wide | awk '{print $1"|"$7}' | grep -v NAME > List

# Itera su ogni host nel file "List"
for entry in $(cat List); do

  host=$(echo $entry | awk -F"|" '{print $1}')
  ip=$(echo $entry | awk -F"|" '{print $2}')

  # Collega tramite SSH utilizzando sshpass per fornire la password
  ssh -l core -i id_rsa -o StrictHostKeyChecking=no -o ConnectTimeout=5 "$ip" \
  "ip -o addr show br-ex | awk '/inet / {print \$2, \$4}' && ip link show br-ex | awk '/link\/ether/ {print \$2}'" > /tmp/info_$host.txt

  # Verifica se il comando ssh è andato a buon fine
  if [ $? -eq 0 ]; then
    # Estrai IP e MAC address
    IP_ADDRESS=$(awk '{print $2}' /tmp/info_$host.txt | head -n 1 | awk -F"/" '{print $1}')
    MAC_ADDRESS=$(awk '/:/ {print $1}' /tmp/info_$host.txt | head -n 1)

    # Mostra le variabili
    echo "$host|$IP_ADDRESS|$MAC_ADDRESS" >> ocp-info.out
    echo "$host - $IP_ADDRESS - $MAC_ADDRESS"
  else
    echo "Errore nel collegamento a $host o interfaccia br-ex non trovata..."
  fi
  
  rm -f /tmp/info_$host.txt

done
