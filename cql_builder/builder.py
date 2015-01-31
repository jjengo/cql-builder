from cql_builder.statement import Insert, Update

'''
TODO 
	- query operation validation
	- item order validation
	- unit tests
'''

class QueryBuilder(object):

	@staticmethod
	def insert_into(keyspace, column_family):
		return Insert(keyspace, column_family)

	@staticmethod
	def update(keyspace, column_family):
		return Update(keyspace, column_family)

if __name__ == '__main__':

	from cassandra.cluster import Cluster
	from cql_builder.assignment import Set
	from cql_builder.condition import *

	keyspace = 'test_keyspace'
	column_family = 'people'
	session = Cluster(['localhost']).connect()

	insert = (QueryBuilder.insert_into(keyspace, column_family)
		.values(first='Jon', last='Jengo', age=32)
		.using(ttl=10800)
	)

	statement, args = insert.statement()	
	print statement, args
	session.execute(statement, args)

	update = (QueryBuilder.update(keyspace, column_family)
		.using(ttl=10800)
		.set(Set(age=45))
		.where(all_eq(last='Jengo', first='Jon'))
	)
	
	statement, args = update.statement()
	print statement, args
	session.execute(statement, args)
