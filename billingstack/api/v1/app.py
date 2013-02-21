# -*- encoding: utf-8 -*-
#
# Copyright © 2013 Woorea Solutions, S.L
#
# Author: Luis Gervaso <luis@woorea.es>
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
"""Set up the API server application instance
"""

import flask

from billingstack.openstack.common import cfg

from billingstack import storage
from billingstack.api.v1 import resources

def make_app(conf, attach_storage=True):
    app = flask.Flask('billingstack.api')
    app.register_blueprint(resources.blueprint, url_prefix='/v1')

    @app.before_request
    def attach_config():
        flask.request.cfg = conf

    if attach_storage:
        @app.before_request
        def attach_storage():
            storage_engine = storage.get_engine(conf['service:api'].storage_driver)
            flask.request.storage_engine = storage_engine
            flask.request.storage_conn = storage_engine.get_connection()

    return app

# For documentation
app = make_app(cfg.CONF, attach_storage=False)