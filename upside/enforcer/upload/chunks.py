from upside.enforcer import config


def adjust_chunk_size(chunks, store):
    """
    If the chunked secret already exists, and the latest update reduces the # of chunks.
    Then an empty terminating value should be appended to the reduced numbers of chunks for history auditing
    """
    if len(chunks) >= len(store):
        return chunks
    else:
        for x in range(len(chunks), len(store)):
            chunks.append(config.CHUNK_TERMINATION_VALUE)
        return chunks


def chunk_secret_value(data, chunk_size):
    """Yield successive chunk_size chunks from data."""
    chunks = []
    for x in range(0, len(data), chunk_size):
        chunks.append(data[x:x + chunk_size])

    return chunks
