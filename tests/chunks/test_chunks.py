from upside.enforcer import config
from upside.enforcer.upload.chunks import chunk_secret_value, adjust_chunk_size
from upside.enforcer.upload.util import add_existing_chunks_to_secret_store
from upside.enforcer.util.secret import Secret


def test_chunking():
    chunks = chunk_secret_value('abcdef', 1)
    assert len(chunks) == 6
    assert chunks[0] == 'a'
    assert chunks[1] == 'b'
    assert chunks[2] == 'c'
    assert chunks[3] == 'd'
    assert chunks[4] == 'e'
    assert chunks[5] == 'f'


def test_adjust_chunk_size_does_not_change():
    store = {
        'test_chunk_000': 'a',
        'test_chunk_001': 'b',
        'test_chunk_002': 'c',
        'test_chunk_003': 'd',
        'test_chunk_004': 'e',
        'test_chunk_005': 'f'
    }

    original_chunks = chunk_secret_value('abcdef', 1)
    updated_chunks = adjust_chunk_size(original_chunks, store)
    for idx, chunk in enumerate(updated_chunks):
        assert original_chunks[idx] == chunk


def test_adjust_chunk_size_reduction():
    store = {
        'test_chunk_000': 'a',
        'test_chunk_001': 'b',
        'test_chunk_002': 'c',
        'test_chunk_003': config.CHUNK_TERMINATION_VALUE,
        'test_chunk_004': config.CHUNK_TERMINATION_VALUE,
        'test_chunk_005': config.CHUNK_TERMINATION_VALUE
    }

    original_chunks = chunk_secret_value('abc', 1)
    updated_chunks = adjust_chunk_size(original_chunks, store)
    for idx, chunk in enumerate(updated_chunks):
        assert original_chunks[idx] == chunk


def test_adjust_chunk_size_increase():
    store = {
        'test_chunk_000': 'a',
        'test_chunk_001': 'b',
        'test_chunk_002': 'c',
        'test_chunk_003': config.CHUNK_TERMINATION_VALUE,
        'test_chunk_004': config.CHUNK_TERMINATION_VALUE,
        'test_chunk_005': config.CHUNK_TERMINATION_VALUE
    }

    original_chunks = chunk_secret_value('abcdefg', 1)
    updated_chunks = adjust_chunk_size(original_chunks, store)

    assert len(updated_chunks) == 7
    assert updated_chunks[0] == 'a'
    assert updated_chunks[1] == 'b'
    assert updated_chunks[2] == 'c'
    assert updated_chunks[3] == 'd'
    assert updated_chunks[4] == 'e'
    assert updated_chunks[5] == 'f'
    assert updated_chunks[6] == 'g'


def test_add_existing_chunks_to_secret_store():
    store = {}
    aws_chunked_secrets = []
    secret = Secret(key='/parent/child', value='test')
    chunks = chunk_secret_value('abcdef', 1)
    for idx, chunk in enumerate(chunks):
        aws_chunked_secrets.append({'Name': '/parent/child' + '_chunk_' + "{:03d}".format(idx), 'Value': chunk})

    add_existing_chunks_to_secret_store({'Parameters': aws_chunked_secrets}, store, secret)

    assert len(store) == 6
    for idx, key_value in enumerate(store.items()):
        assert key_value[0] == secret.name + '_chunk_' + "{:03d}".format(idx)
        assert key_value[1] == chunks[idx]


def test_add_existing_chunks_to_secret_store_wrong_key():
    store = {}
    aws_chunked_secrets = []
    secret = Secret(key='/parent/step_child', value='test')
    chunks = chunk_secret_value('abcdef', 1)
    for idx, chunk in enumerate(chunks):
        aws_chunked_secrets.append({'Name': '/parent/child' + '_chunk_' + "{:03d}".format(idx), 'Value': chunk})

    add_existing_chunks_to_secret_store({'Parameters': aws_chunked_secrets}, store, secret)

    assert len(store) == 0
