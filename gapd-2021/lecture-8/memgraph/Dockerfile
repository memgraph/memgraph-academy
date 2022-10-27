FROM memgraph/memgraph-mage

USER memgraph

# Copy the stream transformation module
COPY transformations/card_fraud.py /usr/lib/memgraph/query_modules
