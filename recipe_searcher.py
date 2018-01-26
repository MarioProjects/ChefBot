## Import de las librerias necesarias para acceder a la api y funcionalidades
import requests
from random import randint

## Parámetros para configuración
api_key = '394c6244e849b9274ef6325cec54f959'
api_base = 'http://food2fork.com/api/'
seach_uri = '{}search?key={}&q={}'

## Funciones de ayuda

def get_recipe(recipe_id):
    # Toma una receta por su identificador
    get_url = '{}/get?key={}&rId={}'.format(api_base, api_key, recipe_id)
    r = requests.get(get_url)
    return r.json()['recipe']


def search_recipe(desired_recipe, ranking_type='r'):
    if ranking_type not in ['r','t']:
        raise Exception("ranking_type must be 'r' or 't'. got {}".format(ranking_type))
    search_url = '{}/search?key={}&q={}&sort={}'.format(api_base, api_key, desired_recipe, ranking_type)
    r = requests.get(search_url)
    if not r.ok:
        raise Exception("error searching for {}: {}".format(desired_recipe, r.test))
    return r.json()



def get_popular_recipes(desired_recipe, ranking_type='r', random=True, num_results=1):
    #print("Finding the {} best recipes for '{}'.".format(num_results, desired_recipe))
    search_results = search_recipe(desired_recipe, ranking_type)
    if search_results['count']:
        for i in range(num_results):
            if random:
                recipeIndx = randint(0, search_results['count'])
            else:
                recipeIndx = i
            recipe_id = search_results['recipes'][recipeIndx]['recipe_id']
            recipe = get_recipe(recipe_id)
            
            #print(recipe['image_url'])
            
            #print("Recipe #{}: {} ({})".format(i+1, recipe['title'], recipe['publisher']))
            print("\n{} ({})".format(recipe['title'], recipe['publisher']))
            print("  url: {}".format(recipe['source_url']))
            print("  ingredients:")
            for ingredient in recipe['ingredients']:
                print("    {}".format(ingredient))
                
    else:
        print("No recipes found.")
