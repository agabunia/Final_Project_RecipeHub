from tests.conftest import login


def test_successful_login(client, user_a):
    """Logging in with correct credentials should succeed and show the recipes page."""
    response = login(client, 'alice@test.com', 'password123')
    assert response.status_code == 200
    assert b'Welcome back' in response.data


def test_failed_login_wrong_password(client, user_a):
    """Logging in with a wrong password should fail with an error message."""
    response = login(client, 'alice@test.com', 'wrong-password')
    assert response.status_code == 200
    assert b'Invalid email or password' in response.data


def test_failed_login_unknown_email(client):
    """Logging in with an email that doesn't exist should fail gracefully, not crash."""
    response = login(client, 'ghost@test.com', 'whatever123')
    assert response.status_code == 200
    assert b'Invalid email or password' in response.data


def test_logout_requires_login_first(client, user_a):
    """After logging in, logout should work and return the user to a logged-out state."""
    login(client, 'alice@test.com', 'password123')
    response = client.get('/auth/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b'You have been logged out' in response.data