from cassandra.cluster import Cluster


cluster = Cluster(['localhost'], port=9043)
session = cluster.connect('shrinkr')

print("Connected to Cassandra cluster:", cluster.metadata.cluster_name)