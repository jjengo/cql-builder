from cassandra.cluster import Cluster
from cassandra import ConsistencyLevel as Level
from cql_builder.assignment import *
from cql_builder.condition import *
from cql_builder.builder import QueryBuilder

if __name__ == '__main__':

	keyspace = 'test_keyspace'
	column_family = 'people'
	session = Cluster(['localhost']).connect()

	# Insert
	insert = (QueryBuilder.insert_into(keyspace, column_family)
		.values(first='foo', last='bar')
		.using(ttl=3600)
	)
	session.execute(*insert.statement(consistency=Level.LOCAL_ONE))

	(QueryBuilder.insert_into(keyspace, column_family)
		.values(first='foo', age=13, friends=['joe', 'schmoe'])
		.using(ttl=10800)
	)

	# Update
	(QueryBuilder.update(keyspace, column_family)
		.using(ttl=3600)
		.set(Set(age=13))
		.where(all_eq(first='foo', last='bar'))
	)

	(QueryBuilder.update(keyspace, column_family)
		.using(ttl=3600)
		.set(Set(age=13))
		.where(
			eq('first', 'foo'),
			eq('last', 'bar')
		)
	)

	(QueryBuilder.update(keyspace, column_family)
		.set(Set(first='foo'))
		.where(
			gt('age', 13),
			lte('age', 25)
		)
	)

	(QueryBuilder.update(keyspace, column_family)
		.set(Set(age=13))
		.where(within('names', ['foo', 'bar']))
	)

	(QueryBuilder.update(keyspace, column_family)
		.set(SetAt('names', 'first', 'foo'))
		.where(all_eq(last='bar'))
	)

	(QueryBuilder.update(keyspace, column_family)
		.set(Add('ages', set([13, 25])))
		.where(eq('last', 'bar'))
	)

	(QueryBuilder.update(keyspace, column_family)
		.set(Set(interests={'sports': 'football', 'language': 'python'}))
		.where(eq('last', 'bar'))
	)
