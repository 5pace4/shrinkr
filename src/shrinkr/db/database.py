from cassandra.cluster import Cluster

from shrinkr.config import settings

app_settings = settings()


cluster = Cluster([app_settings.cassandra_host], port=app_settings.cassandra_port)
session = cluster.connect()

session.execute(
	f"""
	CREATE KEYSPACE IF NOT EXISTS {app_settings.cassandra_keyspace}
	WITH replication = {{'class': 'SimpleStrategy', 'replication_factor': 1}}
	"""
)

session.set_keyspace(app_settings.cassandra_keyspace)

session.execute(
	"""
	CREATE TABLE IF NOT EXISTS users (
		id uuid PRIMARY KEY,
		username text,
		email text,
		password text,
		created_at timestamp
	)
	"""
)

session.execute(
	"""
	CREATE TABLE IF NOT EXISTS urls_by_user (
		user_id uuid,
		short_url text,
		long_url text,
		creation_date timestamp,
		expiration_date timestamp,
		click_count int,
		PRIMARY KEY (user_id, short_url)
	)
	"""
)

session.execute(
	"""
	CREATE INDEX IF NOT EXISTS users_email_idx
	ON users (email)
	"""
)

session.execute(
	"""
	CREATE INDEX IF NOT EXISTS urls_by_user_short_url_idx
	ON urls_by_user (short_url)
	"""
)

print("Connected to Cassandra cluster:", cluster.metadata.cluster_name)