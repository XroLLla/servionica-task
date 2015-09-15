from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import MetaData
from sqlalchemy import ForeignKey
from sqlalchemy import BigInteger
from sqlalchemy import Text
from sqlalchemy import DateTime
from nova.db.sqlalchemy.models import ComputeNode
from nova.db.sqlalchemy.models import Instance

meta = MetaData()
compute_node_stats = Table(
    'compute_node_stats', meta,
    Column('id', Integer, primary_key=True),
    Column('compute_id', Integer, ForeignKey(ComputeNode.id), nullable=False),
    Column('memory_total', Integer),
    Column('cpu_used_percent', Integer),
    Column('updated_at', DateTime),
    Column('deleted_at', DateTime),
    Column('created_at', DateTime),
    Column('deleted', Integer),
    Column('memory_used', Integer)
 )
instance_stats = Table(
    'instance_stats', meta,
    Column('id', Integer, primary_key=True),
    Column('instance_uuid', Text, ForeignKey(Instance.uuid), nullable=False),
    Column('libvirt_id', Integer),
    Column('cpu_time', BigInteger),
    Column('prev_cpu_time', BigInteger),
    Column('mem', Integer),
    Column('prev_updated_at', DateTime),
    Column('updated_at', DateTime),
    Column('deleted_at', DateTime),
    Column('created_at', DateTime),
    Column('deleted', Integer),
    Column('block_dev_iops', BigInteger),
    Column('prev_block_dev_iops', BigInteger),
 )


def upgrade(migrate_engine):
    meta.bind = migrate_engine
    compute_node_stats.create()
    instance_stats.create()


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    compute_node_stats.drop()
    instance_stats.drop()