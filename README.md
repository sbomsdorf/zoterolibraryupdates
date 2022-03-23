# Zotero library updates
Small tool to be run on a Linux server to send regular emails containing new items in a Zotero library.

## Register Application with Zotero 
1. Go to https://www.zotero.org/oauth/apps and click "Register new application"
2. Fill the form. The application type is "client".
3. Copy the client key and the client secret to the config.yaml.

## Create an API key:
1. Go to https://www.zotero.org/settings/keys/new and fill the form depending on your needs. In general,
only read access is necessary.
2. The userID (id in the config.yaml) can be found at https://www.zotero.org/settings/keys. 

For further instructions, see https://www.zotero.org/support/dev/web_api/v3/basics.