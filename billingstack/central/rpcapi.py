# -*- encoding: utf-8 -*-
#
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
from oslo.config import cfg

from billingstack.openstack.common.rpc import proxy

rpcapi_opts = [
    cfg.StrOpt('central_topic', default='central',
               help='the topic central nodes listen on')
]

cfg.CONF.register_opts(rpcapi_opts)


class CentralAPI(proxy.RpcProxy):
    BASE_RPC_VERSION = '1.0'

    def __init__(self):
        super(CentralAPI, self).__init__(
            topic=cfg.CONF.central_topic,
            default_version=self.BASE_RPC_VERSION)

    # Currency
    def create_currency(self, ctxt, values):
        return self.call(ctxt, self.make_msg('create_currency', values=values))

    def list_currencies(self, ctxt, criterion=None):
        return self.call(ctxt, self.make_msg('list_currencies',
                         criterion=criterion))

    def get_currency(self, ctxt, id_):
        return self.call(ctxt, self.make_msg('get_currency',
                         id_=id_))

    def update_currency(self, ctxt, id_, values):
        return self.call(ctxt, self.make_msg('update_currency',
                         id_=id_, values=values))

    def delete_currency(self, ctxt, id_):
        return self.call(ctxt, self.make_msg('delete_currency',
                         id_=id_))

    # Language
    def create_language(self, ctxt, values):
        return self.call(ctxt, self.make_msg('create_language', values=values))

    def list_languages(self, ctxt, criterion=None):
        return self.call(ctxt, self.make_msg('list_languages',
                         criterion=criterion))

    def get_language(self, ctxt, id_):
        return self.call(ctxt, self.make_msg('get_language', id_=id_))

    def update_language(self, ctxt, id_, values):
        return self.call(ctxt, self.make_msg('update_language',
                         id_=id_, values=values))

    def delete_language(self, ctxt, id_):
        return self.call(ctxt, self.make_msg('delete_language', id_=id_))

    # Contact Info
    def create_contact_info(self, ctxt, id_, values):
        return self.call(ctxt, self.make_msg('create_contact_info', id_=id_,
                         values=values))

    def get_contact_info(self, ctxt, id_):
        return self.call(ctxt, self.make_msg('get_contact_info', id_))

    def update_contact_info(self, ctxt, id_, values):
        return self.call(ctxt, self.make_msg('update_contact_info', id_=id_,
                         values=values))

    def delete_contact_info(self, ctxt, id_):
        return self.call(ctxt, self.make_msg('delete_contact_info', id_=id_))

    # Merchant
    def create_merchant(self, ctxt, values):
        return self.call(ctxt, self.make_msg('create_merchant', values=values))

    def list_merchants(self, ctxt, criterion=None):
        return self.call(ctxt, self.make_msg('list_merchants',
                         criterion=criterion))

    def get_merchant(self, ctxt, id_):
        return self.call(ctxt, self.make_msg('get_merchant', id_=id_))

    def update_merchant(self, ctxt, id_, values):
        return self.call(ctxt, self.make_msg('update_merchant',
                         id_=id_, values=values))

    def delete_merchant(self, ctxt, id_):
        return self.call(ctxt, self.make_msg('delete_merchant',
                         id_=id_))

    # Customer
    def create_customer(self, ctxt, merchant_id, values):
        return self.call(ctxt, self.make_msg('create_customer',
                         merchant_id=merchant_id, values=values))

    def list_customers(self, ctxt, criterion=None):
        return self.call(ctxt, self.make_msg('list_customers',
                         criterion=criterion))

    def get_customer(self, ctxt, id_):
        return self.call(ctxt, self.make_msg('get_customer', id_=id_))

    def update_customer(self, ctxt, id_, values):
        return self.call(ctxt, self.make_msg('update_customer',
                         id_=id_, values=values))

    def delete_customer(self, ctxt, id_):
        return self.call(ctxt, self.make_msg('delete_customer', id_=id_))

    # Plans
    def create_plan(self, ctxt, merchant_id, values):
        return self.call(ctxt, self.make_msg('create_plan',
                         merchant_id=merchant_id, values=values))

    def list_plans(self, ctxt, criterion=None):
        return self.call(ctxt, self.make_msg('list_plans',
                         criterion=criterion))

    def get_plan(self, ctxt, id_):
        return self.call(ctxt, self.make_msg('get_plan', id_=id_))

    def update_plan(self, ctxt, id_, values):
        return self.call(ctxt, self.make_msg('update_plan', id_=id_,
                         values=values))

    def delete_plan(self, ctxt, id_):
        return self.call(ctxt, self.make_msg('delete_plan', id_=id_))

    def get_plan_by_subscription(self, ctxt, id_):
        return self.call(ctxt, self.make_msg('get_plan_by_subscription',
                         id_=id_))

    # PlanItems
    def create_plan_item(self, ctxt, values):
        return self.call(ctxt, self.make_msg('create_plan_item',
                         values=values))

    def list_plan_items(self, ctxt, criterion=None):
        return self.call(ctxt, self.make_msg('list_plan_items',
                         criterion=criterion))

    def get_plan_item(self, ctxt, plan_id, product_id):
        return self.call(ctxt, self.make_msg('get_plan_item',
                         plan_id=plan_id, product_id=product_id))

    def update_plan_item(self, ctxt, plan_id, product_id, values):
        return self.call(ctxt, self.make_msg('update_plan_item',
                         plan_id=plan_id, product_id=product_id,
                         values=values))

    def delete_plan_item(self, ctxt, plan_id, product_id):
        return self.call(ctxt, self.make_msg('delete_plan_item',
                         plan_id=plan_id, product_id=product_id))

    # Products
    def create_product(self, ctxt, merchant_id, values):
        return self.call(ctxt, self.make_msg('create_product',
                         merchant_id=merchant_id, values=values))

    def list_products(self, ctxt, criterion=None):
        return self.call(ctxt, self.make_msg('list_products',
                         criterion=criterion))

    def get_product(self, ctxt, id_):
        return self.call(ctxt, self.make_msg('get_product', id_=id_))

    def update_product(self, ctxt, id_, values):
        return self.call(ctxt, self.make_msg('update_product', id_=id_,
                         values=values))

    def delete_product(self, ctxt, id_):
        return self.call(ctxt, self.make_msg('delete_product', id_=id_))

    # Subscriptions
    def create_subscription(self, ctxt, values):
        return self.call(ctxt, self.make_msg('create_subscription',
                         values=values))

    def list_subscriptions(self, ctxt, criterion=None):
        return self.call(ctxt, self.make_msg('list_subscriptions',
                         criterion=criterion))

    def get_subscription(self, ctxt, id_):
        return self.call(ctxt, self.make_msg('get_subscription', id_=id_))

    def update_subscription(self, ctxt, id_, values):
        return self.call(ctxt, self.make_msg('update_subscription', id_=id_,
                         values=values))

    def delete_subscription(self, ctxt, id_):
        return self.call(ctxt, self.make_msg('delete_subscription', id_=id_))


central_api = CentralAPI()
