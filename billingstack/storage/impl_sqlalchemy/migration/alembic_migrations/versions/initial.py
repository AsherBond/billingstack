# vim: tabstop=4 shiftwidth=4 softtabstop=4
#
# Copyright 2013 OpenStack LLC
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
#

"""empty message

Revision ID: 257f3300a0c3
Revises: None
Create Date: 2013-02-09 21:48:52.846656

"""


# revision identifiers, used by Alembic.
revision = '257f3300a0c3'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('invoice_state',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('name', sa.Unicode(length=40), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('language',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('code', sa.Unicode(length=10), nullable=True),
    sa.Column('name', sa.Unicode(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('currency',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('code', sa.Unicode(length=10), nullable=True),
    sa.Column('name', sa.Unicode(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('invoice_line',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('description', sa.Unicode(length=255), nullable=True),
    sa.Column('price', sa.Float(), nullable=True),
    sa.Column('quantity', sa.Float(), nullable=True),
    sa.Column('sub_total', sa.Float(), nullable=True),
    sa.Column('invoice_id', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['invoice_id'], ['currency.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('account',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('account_type', sa.Unicode(length=20), nullable=False),
    sa.Column('name', sa.Unicode(length=60), nullable=False),
    sa.Column('currency_id', sa.UUID(), nullable=True),
    sa.Column('language_id', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['currency_id'], ['currency.id'], ),
    sa.ForeignKeyConstraint(['language_id'], ['language.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('merchant',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.ForeignKeyConstraint(['id'], ['account.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('product',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('name', sa.Unicode(length=60), nullable=False),
    sa.Column('title', sa.Unicode(length=100), nullable=True),
    sa.Column('description', sa.Unicode(length=255), nullable=True),
    sa.Column('measure', sa.Unicode(length=255), nullable=True),
    sa.Column('source', sa.Unicode(length=255), nullable=True),
    sa.Column('type', sa.Unicode(length=255), nullable=True),
    sa.Column('price', sa.Float(), nullable=True),
    sa.Column('merchant_id', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['merchant_id'], ['merchant.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('username', sa.Unicode(length=20), nullable=False),
    sa.Column('password', sa.Unicode(length=255), nullable=False),
    sa.Column('api_key', sa.Unicode(length=255), nullable=True),
    sa.Column('api_secret', sa.Unicode(length=255), nullable=True),
    sa.Column('merchant_id', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['merchant_id'], ['merchant.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('customer',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('merchant_id', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['id'], ['account.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['merchant_id'], ['merchant.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('plan',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('name', sa.Unicode(length=60), nullable=True),
    sa.Column('title', sa.Unicode(length=100), nullable=True),
    sa.Column('description', sa.Unicode(length=255), nullable=True),
    sa.Column('provider', sa.Unicode(length=255), nullable=True),
    sa.Column('merchant_id', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['merchant_id'], ['merchant.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('payment_gateway',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('name', sa.Unicode(length=60), nullable=True),
    sa.Column('title', sa.Unicode(length=100), nullable=True),
    sa.Column('description', sa.Unicode(length=255), nullable=True),
    sa.Column('is_default', sa.Boolean(), nullable=True),
    sa.Column('merchant_id', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['merchant_id'], ['merchant.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('subscription',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('billing_day', sa.Integer(), nullable=True),
    sa.Column('payment_method', sa.Unicode(length=255), nullable=True),
    sa.Column('resource', sa.Unicode(length=255), nullable=True),
    sa.Column('plan_id', sa.UUID(), nullable=True),
    sa.Column('merchant_id', sa.UUID(), nullable=True),
    sa.Column('customer_id', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['customer_id'], ['customer.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['merchant_id'], ['merchant.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['plan_id'], ['plan.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_customer_roles',
    sa.Column('user_id', sa.UUID(), nullable=True),
    sa.Column('customer_id', sa.UUID(), nullable=True),
    sa.Column('role', sa.Unicode(length=40), nullable=True),
    sa.ForeignKeyConstraint(['customer_id'], ['customer.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint()
    )
    op.create_table('plan_item',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('name', sa.Unicode(length=60), nullable=True),
    sa.Column('title', sa.Unicode(length=100), nullable=True),
    sa.Column('description', sa.Unicode(length=255), nullable=True),
    sa.Column('price', sa.Float(), nullable=True),
    sa.Column('value_from', sa.Float(), nullable=True),
    sa.Column('value_to', sa.Float(), nullable=True),
    sa.Column('plan_id', sa.UUID(), nullable=True),
    sa.Column('merchant_id', sa.UUID(), nullable=True),
    sa.Column('product_id', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['merchant_id'], ['merchant.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['plan_id'], ['plan.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['product_id'], ['product.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_customer',
    sa.Column('user_id', sa.UUID(), nullable=True),
    sa.Column('customer_id', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['customer_id'], ['customer.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint()
    )
    op.create_table('invoice',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('identifier', sa.Unicode(length=255), nullable=False),
    sa.Column('due', sa.DateTime(), nullable=True),
    sa.Column('sub_total', sa.Float(), nullable=True),
    sa.Column('tax_percentage', sa.Float(), nullable=True),
    sa.Column('tax_total', sa.Float(), nullable=True),
    sa.Column('total', sa.Float(), nullable=True),
    sa.Column('customer_id', sa.UUID(), nullable=True),
    sa.Column('state_id', sa.UUID(), nullable=True),
    sa.Column('currency_id', sa.UUID(), nullable=True),
    sa.Column('merchant_id', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['currency_id'], ['currency.id'], ),
    sa.ForeignKeyConstraint(['customer_id'], ['customer.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['merchant_id'], ['merchant.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['state_id'], ['invoice_state.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('contact_info',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('address1', sa.Unicode(length=60), nullable=True),
    sa.Column('address2', sa.Unicode(length=60), nullable=True),
    sa.Column('city', sa.Unicode(length=60), nullable=True),
    sa.Column('company', sa.Unicode(length=60), nullable=True),
    sa.Column('country', sa.Unicode(length=40), nullable=True),
    sa.Column('state', sa.Unicode(length=40), nullable=True),
    sa.Column('zip', sa.Unicode(length=20), nullable=True),
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('usage',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('measure', sa.Unicode(length=255), nullable=True),
    sa.Column('start_timestamp', sa.DateTime(), nullable=True),
    sa.Column('end_timestamp', sa.DateTime(), nullable=True),
    sa.Column('price', sa.Float(), nullable=True),
    sa.Column('total', sa.Float(), nullable=True),
    sa.Column('value', sa.Float(), nullable=True),
    sa.Column('subscription_id', sa.UUID(), nullable=True),
    sa.Column('merchant_id', sa.UUID(), nullable=True),
    sa.Column('customer_id', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['customer_id'], ['customer.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['merchant_id'], ['merchant.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['subscription_id'], ['subscription.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('usage')
    op.drop_table('contact_info')
    op.drop_table('invoice')
    op.drop_table('user_customer')
    op.drop_table('plan_item')
    op.drop_table('user_customer_roles')
    op.drop_table('subscription')
    op.drop_table('payment_gateway')
    op.drop_table('plan')
    op.drop_table('customer')
    op.drop_table('user')
    op.drop_table('product')
    op.drop_table('merchant')
    op.drop_table('account')
    op.drop_table('invoice_line')
    op.drop_table('currency')
    op.drop_table('language')
    op.drop_table('invoice_state')
    ### end Alembic commands ###
