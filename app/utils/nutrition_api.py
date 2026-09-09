import requests
from flask import current_app


class NutritionAPIError(Exception):
    """Custom exception for Nutrition API errors."""
    pass


def get_nutrition_estimate(dish_title):
    """
    Calls Spoonacular's guessNutrition endpoint.
    Returns a dict with calories/protein/fat/carbs, or raises NutritionAPIError.
    """
    api_key = current_app.config.get('SPOONACULAR_API_KEY')

    if not api_key:
        raise NutritionAPIError('No Spoonacular API key configured.')

    url = 'https://api.spoonacular.com/recipes/guessNutrition'
    params = {'title': dish_title, 'apiKey': api_key}

    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()

        return {
            'calories': data.get('calories', {}).get('value'),
            'protein': data.get('protein', {}).get('value'),
            'fat': data.get('fat', {}).get('value'),
            'carbs': data.get('carbs', {}).get('value'),
        }

    except requests.exceptions.Timeout:
        current_app.logger.error(f'Nutrition API timeout for "{dish_title}"')
        raise NutritionAPIError('The nutrition service took too long to respond.')

    except requests.exceptions.HTTPError as e:
        current_app.logger.error(f'Nutrition API HTTP error for "{dish_title}": {e}')
        raise NutritionAPIError('The nutrition service returned an error.')

    except requests.exceptions.RequestException as e:
        current_app.logger.error(f'Nutrition API request failed for "{dish_title}": {e}')
        raise NutritionAPIError('Could not reach the nutrition service.')




