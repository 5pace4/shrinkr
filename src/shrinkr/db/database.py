from cassandra.cluster import Cluster

from shrinkr.config import settings

app_settings = settings()


cluster = Cluster([app_settings.cassandra_host], port=app_settings.cassandra_port)
session = cluster.connect(app_settings.cassandra_keyspace)

session.execute(
	"""
	CREATE INDEX IF NOT EXISTS users_email_idx
	ON users (email)
	"""
)

print("Connected to Cassandra cluster:", cluster.metadata.cluster_name)