#!/bin/bash

# Ugly bash script to:
# - get all images from a given root directory in Dropbox
# - delete one or more images from Dropbox, given a string that match the image to be deleted

token="hTgNwCeeqeAAAAAAAAAAAX_gw1mfcyHOABpyzCialBAr6I6GW22RsbEJp_Vjofm4"
rootDirectory="/Otalio_images"

function get {

  > list_dropbox_files

  # get list of files and directory
  RESPONSE=$(curl -X POST https://api.dropboxapi.com/2/files/list_folder --header "Authorization: Bearer $token" --header "Content-Type: application/json" --data "{\"path\": \"$rootDirectory\"}")

  # files under root directory, go to final list
  echo "$RESPONSE" | jq -r '.entries[] | select(.".tag" == "file") | .path_display' >> list_dropbox_files

  # subfolders need to be queried again
  echo "$RESPONSE" | jq -r '.entries[] | select(.".tag" == "folder") | .name' > list_dropbox_folders

  for folder in $(cat list_dropbox_folders); do
    for file in $(curl -X POST https://api.dropboxapi.com/2/files/list_folder --header "Authorization: Bearer $token" --header "Content-Type: application/json" --data "{\"path\": \"${rootDirectory}/${folder}\"}" | jq '.entries[].path_display' | sed -e 's/"//g'); do
      echo $file >> list_dropbox_files
    done
  done

}

function delete {

  if [ ! -f list_dropbox_files ]; then
    echo "First of all, run: $0 get"
    exit 1
  fi

  list=$(cat list_dropbox_files | grep $string)

  echo $list | sed -e 's/\ /\n/g'
  echo -n "Proceed with removal? [yes/no]: "
  read -r human

  if [ $human == "no" ] || [ $human == "n" ]; then
    exit 0
  elif [ $human == "yes" ] || [ $human == "y" ]; then
    for file in $list; do
      curl -X POST https://api.dropboxapi.com/2/files/delete --header "Authorization: Bearer $token" --header "Content-Type: application/json" --data "{\"path\": \"$file\"}"
    done
  else
    echo "Answer not correct"
    exit 1
  fi

}

action=$1

if [ -z $action ]; then
  echo "Action to be set [get|delete]"
  exit 1
fi

if [ $action == "get" ]; then
  get
elif [ $action == "delete" ]; then
  string=$2
  if [ -z $string ]; then
    echo "Need a string to delete files"
    exit 1
  fi
  delete
else
  echo "Action not correct [get|delete]"
fi

