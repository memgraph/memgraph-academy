# Start Memgraph Platform
# docker run -it -p 7687:7687 -p 7444:7444 -p 3000:3000 memgraph/memgraph-platform

from gqlalchemy import Memgraph

memgraph = Memgraph()


results = memgraph.execute_and_fetch(
    """
    MATCH (n) RETURN count(n) AS number_of_nodes ;
    """
)
print(next(results))
