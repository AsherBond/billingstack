"""
A service that does calls towards the PGP web endpoint or so
"""

import functools
import re
from oslo.config import cfg
from billingstack.openstack.common import log as logging
from billingstack.openstack.common import rpc
from billingstack.openstack.common.rpc import service as rpc_service
from stevedore.named import NamedExtensionManager
from billingstack import exceptions
from billingstack import utils
from billingstack.central.rpcapi import CentralAPI


cfg.CONF.import_opt('host', 'billingstack.netconf')
cfg.CONF.import_opt('host', 'billingstack.payment_gateway.rpcapi')

LOG = logging.getLogger(__name__)


class Service(rpc_service.Service):
    def __init__(self, *args, **kwargs):
        kwargs.update(
            host=cfg.CONF.host,
            topic=cfg.CONF.central_topic,
        )

        super(Service, self).__init__(*args, **kwargs)

        # Get a storage connection
        self.central_api = CentralAPI()

    def pg_provider_get(self, ctxt, pg_info):
        """
        Work out a PGC config either from pg_info or via ctxt fetching it from central.
        Return the appropriate PGP for this info.

        :param ctxt: Request context
        :param pg_info: Payment Gateway Config...
        """

    def account_add(self, ctxt, values, pg_config=None):
        """
        Create an Account on the underlying provider

        :param values: The account values
        """

    def __getattr__(self, name):
        """
        Proxy onto the storage api if there is no local method present..

        For now to avoid to have to write up every method once more here...
        """
        if hasattr(self, name):
            return getattr(self, name)

        f = getattr(self.provider, name)
        if not f:
            raise AttributeError

        @functools.wraps(f)
        def _wrapper(*args, **kw):
            return f(*args, **kw)
        setattr(self, name, _wrapper)
        return _wrapper