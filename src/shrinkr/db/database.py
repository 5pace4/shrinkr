from cassandra.cluster import Cluster


cluster = Cluster(['localhost'], port=9043)
session = cluster.connect('shrinkr')

session.execute(
	"""
	CREATE INDEX IF NOT EXISTS users_email_idx
	ON users (email)
	"""
)

print("Connected to Cassandra cluster:", cluster.metadata.cluster_name)