#!/bin/sh

# use curl to load initial templates and/or configuration
echo "POST template to " $XLR_HOST
# curl  -u admin:admin 'http://xld:5516/api/v1/phases/Applications/Release1a/phase' -i -X POST -H 'Content-Type: application/json' -H 'Accept: application/json' -d @/tmp/data/release-template-variableSetter.json

echo "init complete..."