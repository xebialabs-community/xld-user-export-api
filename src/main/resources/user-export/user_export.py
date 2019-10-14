#
# Copyright 2019 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

# Import common Python modules as needed
import os.path
import sys
import logging
import re

logging.basicConfig(filename='log/custom-api.log',
                            filemode='a',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.DEBUG)

logging.debug("main: begin")

users = {}

# https://docs.xebialabs.com/xl-deploy/8.5.x/javadoc/engine-api/com/xebialabs/deployit/engine/api/RoleService.html
# Returns: a List of RolePrinciple objects
#   RolePrinciple: Role, List<String> principles
#       Role: id, name
roles = roleService.readRolePrincipals()
for rp in roles:
    logging.debug(rp)

    # get permissions for role
    # https://docs.xebialabs.com/xl-deploy/8.5.x/javadoc/engine-api/com/xebialabs/deployit/engine/api/PermissionService.html
    # Returns: a Map of configuration item ids to permissions granted to the user. 'global' is a special ci
    permissions = permissionService.getGrantedPermissions(rp.role.name)
    logging.debug(permissions)

    for p in rp.principals:
        if not p in users:
            users[p] = {}
            users[p]['roles'] = []

        role = {}
        role['role'] = rp.role.name
        role['permissions'] = permissions
        users[p]['roles'].append(role)

# form response
response.statusCode = 200
response.entity = {
    "users": users
}

logging.debug("main: end")
