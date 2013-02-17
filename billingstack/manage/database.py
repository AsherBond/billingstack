# Author: Endre Karlson <endre.karlson@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.


from billingstack.openstack.common import cfg
from billingstack.openstack.common import log
from billingstack.manage.base import Command
from billingstack.storage import get_connection


LOG = log.getLogger(__name__)


cfg.CONF.import_opt('storage_driver', 'billingstack.api',
                    group='service:api')
cfg.CONF.import_opt('database_connection', 'billingstack.storage.impl_sqlalchemy',
                    group='storage:sqlalchemy')


class DatabaseCommand(Command):
    """
    A Command that uses a storage connection to do some stuff
    """
    def setup(self, parsed_args):
        self.conn = get_connection()