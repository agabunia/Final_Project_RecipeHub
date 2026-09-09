# tests/test_permissions.py
from tests.conftest import login


def test_cannot_edit_someone_elses_recipe(client, user_a, user_b, recipe_by_a):
    """User B should get a 403 when trying to edit User A's recipe."""
    login(client, 'bob@test.com', 'password123')

    response = client.get(f'/recipes/{recipe_by_a.id}/edit')
    assert response.status_code == 403


def test_cannot_delete_someone_elses_recipe(client, user_a, user_b, recipe_by_a, db):
    """User B should get a 403 when trying to delete User A's recipe, and it should still exist."""
    login(client, 'bob@test.com', 'password123')

    response = client.post(f'/recipes/{recipe_by_a.id}/delete')
    assert response.status_code == 403

    # confirm the recipe was NOT actually deleted
    from app.models import Recipe
    still_exists = db.session.get(Recipe, recipe_by_a.id)
    assert still_exists is not None


def test_owner_can_edit_own_recipe(client, user_a, recipe_by_a):
    """Sanity check: the actual owner CAN access the edit page (proves the 403s above are about ownership, not a broken route)."""
    login(client, 'alice@test.com', 'password123')

    response = client.get(f'/recipes/{recipe_by_a.id}/edit')
    assert response.status_code == 200