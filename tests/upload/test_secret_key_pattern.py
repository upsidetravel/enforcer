from pytest import raises

from upside.enforcer.upload.util import secret_key_pattern


def test_good_pattern():
    assert secret_key_pattern('/test/test') == '/test/test'
    assert secret_key_pattern('/test_test.-test/test.test-test') == '/test_test.-test/test.test-test'


def test_value_error():
    with raises(Exception) as err:
        secret_key_pattern('/test/')
    assert err.typename == 'ValueError'


def test_bad_pattern():
    with raises(ValueError):
        secret_key_pattern('/test/')

    with raises(ValueError):
        secret_key_pattern('test')

    with raises(ValueError):
        secret_key_pattern('test/')

    with raises(ValueError):
        secret_key_pattern('test/test')

    with raises(ValueError):
        secret_key_pattern('test_test.-test/test.test-test')

    with raises(ValueError):
        secret_key_pattern('/test_/test.-test/test.test-test')

    with raises(ValueError):
        secret_key_pattern('/test/test/')

    with raises(ValueError):
        secret_key_pattern('/te$t/test')
