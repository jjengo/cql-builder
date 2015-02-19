from cassandra.cluster import Cluster
from cassandra import ConsistencyLevel as Level
from cql_builder.builder import QueryBuilder
from cql_builder.condition import *

if __name__ == '__main__':

	keyspace = 'test_keyspace'
	column_family = 'people'
	session = Cluster(['localhost']).connect()

	# INSERT INTO ... (first, last) VALUES (foo, bar) USING TTL 3600
	insert = (QueryBuilder.insert_into(keyspace, column_family)
		.values(first='foo', last='bar')
		.using(ttl=3600)
	)
	session.execute(*insert.statement(consistency=Level.LOCAL_ONE))

	# INSERT INTO ... (first, age, friends) VALUES (foo, 13, ['joe', 'schmoe']) USING TTL 10800
	(QueryBuilder.insert_into(keyspace, column_family)
		.values(first='foo', age=13, friends=['joe', 'schmoe'])
		.using(ttl=10800)
	)

	# UPDATE ... USING TTL 3600 SET age=13 WHERE first='foo' AND last='bar'
	(QueryBuilder.update(keyspace, column_family)
		.using(ttl=3600)
		.set(age=13)
		.where(all_eq(first='foo', last='bar'))
	)

	# UPDATE ... USING TTL 3600 SET age=13 WHERE first='foo' AND last='bar'
	(QueryBuilder.update(keyspace, column_family)
		.using(ttl=3600)
		.set(age=13)
		.where(
			eq('first', 'foo'),
			eq('last', 'bar')
		)
	)

	# UPDATE ... SET first='foo' WHERE age>13 AND age<=15
	(QueryBuilder.update(keyspace, column_family)
		.set(first='foo')
		.where(
			gt('age', 13),
			lte('age', 25)
		)
	)

	# UPDATE ... SET age=13 WHERE names IN ('foo', 'bar')
	(QueryBuilder.update(keyspace, column_family)
		.set(age=13)
		.where(within('names', ['foo', 'bar']))
	)

	# UPDATE ... SET names['first'] = 'foo' WHERE last='bar'
	(QueryBuilder.update(keyspace, column_family)
		.set_at('names', 'first', 'foo')
		.where(all_eq(last='bar'))
	)

	# UPDATE ... SET ages=ages + {13, 15} WHERE last='bar'
	(QueryBuilder.update(keyspace, column_family)
		.add('ages', set([13, 25]))
		.where(eq('last', 'bar'))
	)

	# UPDATE ... SET friends=friends - ['baz'] WHERE last='bar'
	(QueryBuilder.update(keyspace, column_family)
		.subtract('friends', ['baz'])
		.where(eq('last', 'bar'))
	)

	# UPDATE ... SET age=13, friends=friends + {'foo'} WHERE LAST='bar'
	(QueryBuilder.update(keyspace, column_family)
		.set(age=13)
		.add('friends', set(['foo']))
		.where(eq('last', 'bar'))
	)

	# UPDATE ... SET interests={'sports': 'football', 'language': 'python'} WHERE last='bar'
	(QueryBuilder.update(keyspace, column_family)
		.set(interests={'sports': 'football', 'language': 'python'})
		.where(eq('last', 'bar'))
	)

	# SELECT * FROM ...
	(QueryBuilder.select_from(keyspace, column_family)
		.all()
	)

	# SELECT * FROM ... WHERE first='foo' AND last='bar'
	(QueryBuilder.select_from(keyspace, column_family)
		.all()
		.where(all_eq(first='foo', last='bar'))
	)

	# SELECT first, last FROM ... WHERE last='bar'
	(QueryBuilder.select_from(keyspace, column_family)
		.columns('first', 'last')
		.where(eq('last', 'bar'))
	)

	# SELECT COUNT(*) FROM
	(QueryBuilder.select_from(keyspace, column_family)
		.count()
	)

	# SELECT first, last FROM ... WHERE last='bar' LIMIT 5
	(QueryBuilder.select_from(keyspace, column_family)
		.columns('first', 'last')
		.where(eq('last', 'bar'))
		.limit(5)
	)

	# DELETE FROM ... WHERE last='bar'
	(QueryBuilder.delete_from(keyspace, column_family)
		.where(eq('last', 'bar'))
	)

	# DELETE friends, interests FROM ... WHERE last='bar'
	(QueryBuilder.delete_from(keyspace, column_family)
		.columns('friends', 'interests')
		.where(eq('last', 'bar'))
	)

	# DELETE interests['sports'] FROM ... WHERE last='bar'
	(QueryBuilder.delete_from(keyspace, column_family)
		.at('interests', 'sports')
		.where(eq('last', 'bar'))
	)
