# XL Deploy User Export API

[![Build Status][xld-user-export-api-travis-image]][xld-user-export-api-travis-url]
[![Codacy Badge][xld-user-export-api-codacy-image] ][xld-user-export-api-codacy-url]
[![Code Climate][xld-user-export-api-code-climate-image] ][xld-user-export-api-code-climate-url]
[![License: MIT][xld-user-export-api-license-image]][xld-user-export-api-license-url]
[![Github All Deploys][xld-user-export-api-downloads-image]]()

## Preface

This document describes the functionality provided by the XL Deploy xld-user-export-api.

See the [XL Deploy reference manual](https://docs.xebialabs.com/xl-Deploy) for background information on XL Deploy and Deploy automation concepts.  

## Overview

This plugin implements a custom REST API that returns users along with their roles and permissions.

## Requirements

* **Requirements**
*  **XL Deploy**   9.0+

## Installation

* Copy the latest JAR file from the [releases page](https://github.com/xebialabs-community/xld-user-export-api/Deploys) into the `XL_DEPLOY_SERVER/plugins/` directory.
* Restart the XL Deploy server.

## Usage

Make an HTTP GET request to https://\<your xl deploy\>/api/extension/user-export/users

The response object is similar to the following...  

```json
{
  "entity": {
    "users": {
      "jsmith": {
        "roles": [
          {
            "role": "ops",
            "permissions": {
              "global": [
                "login",
                "security#edit",
                "controltask#execute"
              ]
            }
          }
        ]
      },
      "tim": {
        "roles": [
          {
            "role": "dev",
            "permissions": {}
          },
          {
            "role": "ops",
            "permissions": {
              "global": [
                "login",
                "security#edit",
                "controltask#execute"
              ]
            }
          }
        ]
      }
    }
  },
  "stdout": "",
  "stderr": "",
  "exception": null
}
```

## Developers

### Prerequisites

1. You will need to have Docker and Docker Compose installed.
2. The XL-Deploy docker container expects to find a valid XL-Deploy license on your machine, at this location: ~/xl-licenses/xl-Deploy-license.lic

### Build and package the plugin

Execute the following from the project root directory...

```bash
./gradlew clean assemble
```

Output will be placed in ./build/libs folder.

### To run integration tests

Execute the following from the project root directory...

```bash
./gradlew clean itest
```

The itest will set up a containerized xld/\<???\> testbed using docker compose.

### To run demo or dev version

```bash
cd ./src/test/resources
docker-compose -f docker/docker-compose.yml up
```

NOTE:

1. XL Deploy will run on the [localhost port 14516](http://localhost:14516/)
2. The XL Deploy username / password is admin / admin

[xld-user-export-api-travis-image]: https://travis-ci.org/xebialabs-community/xld-user-export-api.svg?branch=master
[xld-user-export-api-travis-url]: https://travis-ci.org/xebialabs-community/xld-user-export-api

[xld-user-export-api-codacy-image]: https://api.codacy.com/project/badge/Grade/88dec34743b84dac8f9aaaa665a99207
[xld-user-export-api-codacy-url]: https://www.codacy.com/app/ladamato/xld-user-export-api

[xld-user-export-api-code-climate-image]: https://codeclimate.com/github/xebialabs-community/xld-user-export-api/badges/gpa.svg
[xld-user-export-api-code-climate-url]: https://codeclimate.com/github/xebialabs-community/xld-user-export-api

[xld-user-export-api-license-image]: https://img.shields.io/badge/License-MIT-yellow.svg
[xld-user-export-api-license-url]: https://opensource.org/licenses/MIT
[xld-user-export-api-downloads-image]: https://img.shields.io/github/downloads/xebialabs-community/xld-user-export-api/total.svg
