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

import com.xebialabs.deployit.engine.api.dto.Paging as Paging
import com.xebialabs.deployit.engine.api.dto.Ordering as Ordering

logging.basicConfig(filename='log/custom-api.log',
                            filemode='a',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.DEBUG)

logging.debug("main: begin")

# process query parameters
filter = None
paging = None
order = Ordering("id:ASC")

if 'userid' in request.query:
    # search for single user
    logging.debug('has query parameter userid=%s' % request.query['userid'])
    filter = request.query['userid']
elif 'page' in request.query:
    logging.debug('get all users')
    page = 0
    if 'page' in request.query:
        page = int(request.query['page'])

    if page < 0:
        page = 0

    resultsPerPage = -1
    if 'resultsPerPage' in request.query:
        resultsPerPage = int(request.query['resultsPerPage'])

    # to make first page = 0 like XLR
    paging = Paging(page+1, resultsPerPage)

# get XLD users...
# https://legacydocs.xebialabs.com/jython-docs/#!/xl-deploy/8.6.x//service/com.xebialabs.deployit.engine.api.UserService#UserService-listUserNames-String-Paging-Ordering
# Returns: a list of user id's
users = userService.listUserNames(filter, paging, order)
logging.debug('users...')
logging.debug(users)

users_out = {}
for p in users:
    users_out[p] = {}
    users_out[p]['roles'] = []

# get XLD roles...
# https://docs.xebialabs.com/xl-deploy/8.5.x/javadoc/engine-api/com/xebialabs/deployit/engine/api/RoleService.html
# Returns: a List of RolePrinciple objects
#   RolePrinciple: Role, List<String> principles
#       Role: id, name

roles = roleService.readRolePrincipals()

roles_out = []
for rp in roles:
    # if we're filtering users, only take roles for those users
    if filter and not filter in rp.principals:
        logging.debug('principal not found in role %s' % rp.role.name)
        continue

    # get permissions for role
    # https://docs.xebialabs.com/xl-deploy/8.5.x/javadoc/engine-api/com/xebialabs/deployit/engine/api/PermissionService.html
    # Returns: a Map of configuration item ids to permissions granted to the user. 'global' is a special ci
    permissions = permissionService.getGrantedPermissions(rp.role.name)

    # format role to json serialization
    role_out = {}
    role_out['role'] = rp.role.name
    role_out['permissions'] = permissions
    role_out['principals'] = rp.principals

    roles_out.append(role_out)

    # add role to user
    for p in rp.principals:
        # could happen is someone is in a role but not in the uers list?
        if not p in users_out:
            logging.warn('principal %s not found in user list' % p)
            users_out[p] = {}
            users_out[p]['roles'] = []

        role = {}
        role['role'] = rp.role.name
        role['permissions'] = permissions

        users_out[p]['roles'].append(role)

# form response
response.statusCode = 200
response.entity = {
    "users": users_out,
    "roles": roles_out
}

logging.debug("main: end")
