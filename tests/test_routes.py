def test_home_redirects_to_recipes(client):
    """The root URL should redirect to the recipes list."""
    response = client.get('/', follow_redirects=True)
    assert response.status_code == 200
    assert b'All Recipes' in response.data


def test_recipes_list_accessible_without_login(client):
    """Anyone, logged in or not, should be able to view the recipes list."""
    response = client.get('/recipes/')
    assert response.status_code == 200


def test_about_page_accessible(client):
    """The About page should be public."""
    response = client.get('/about')
    assert response.status_code == 200
    assert b'About Recipe Portal' in response.data


def test_nonexistent_route_returns_404(client):
    """An unknown URL should trigger the custom 404 handler."""
    response = client.get('/this-route-does-not-exist')
    assert response.status_code == 404
    assert b'Page Not Found' in response.data


def test_add_recipe_requires_login(client):
    """Anonymous users should be redirected away from Add Recipe, not shown the form."""
    response = client.get('/recipes/add', follow_redirects=True)
    assert response.status_code == 200
    assert b'Login' in response.data