"""
Module with search-related utility functions and classes
"""

# ES String query https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-query-string-query.html

# es = Elasticsearch(esurl)
# ess = Search(using=es, index="myindex")
# q1 = ess.query("match", field_name="value")
# q1.to_dict()  # show query json
# res1 = q1.execute()  # iterable of Hit objects
# res1.hits # list of Hit objects
# h0 = res1.hits[0]
# h0.field  # all fields directly accessible as attributes
# h0["field"] # same but works if fields contain illegal chars
# # nested fields can be a list of dict
# list(hit in q1.scan()   # should return all hits!!
#
# !!!! API very different between version 7 and version 8!!!!

# doc1 = es.get(index="myindex", id=myid)  # returns dict, the actual data is in key _source
# Directly sending a search request to es
# see https://elasticsearch-py.readthedocs.io/en/v8.1.3/api.html#elasticsearch.Elasticsearch.search
# res2 = es.search(index="myindex", query=dict(match_all={}), size=1000)  # returns dict
# res2 has keys: took, timed_out, _shards, hits
# res2["hits"] has keys total, max_score, hits
# res2["hits"]["total"] # => {"value": 10000, "relation": gte}  # may not return exact number!!!!!!
# res2["hits"]["hits"]   # only contains 10 by default or size as specified with search
# https://elasticsearch-py.readthedocs.io/en/v7.16.2/api.html#elasticsearch.Elasticsearch.scroll
# see https://elasticsearch-py.readthedocs.io/en/v8.1.3/api.html#elasticsearch.Elasticsearch.scroll
#
# see https://elasticsearch-py.readthedocs.io/en/master/helpers.html?highlight=scan#scan
# res3 = elasticsearch.helpers.scan(es, query=myquery, scroll="5m", preserve_order=False,

# See https://www.elastic.co/guide/en/elasticsearch/reference/master/paginate-search-results.html#search-after
# see https://www.elastic.co/guide/en/elasticsearch/reference/master/paginate-search-results.html#scroll-search-results
# Apparently scroll was done until version 7, but in verison 8 we should use point in time and search_after

# basic strategy:
# r=es.open_point_in_time(index=myindex, keep_alive="2m")
# pit_id = r["id"]
# pit_clause = { "id": pit_id, "keep_alive": "1m" }
# resp = es.search(query=myquery, size=n, pit=pit_clause)
# other solution with complex body: https://github.com/elastic/elasticsearch-py/issues/733
# Proper protocol explained here:
# https://www.elastic.co/guide/en/elasticsearch/reference/current/paginate-search-results.html#search-after

# FOR SLOW BROWSING MAYBE BEST: use search after protocol to quickly retrieve all document ids and store
# (when searching, specify that we only want the id, nothing else from _source, or retrieve only the stuff
# shown in the hit list for all matching documents.
# Then, if we need full info, retrieve individual docs by id

import elasticsearch7 as es
from time import sleep
