from upside.enforcer.util.secret import Secret


def test_secret():
    secret = Secret(key='/parent/child', value='test')
    assert secret.parent_directory == 'parent'
    assert secret.key == '/parent/child'
    assert secret.value == 'test'
    assert secret.name == 'child'
