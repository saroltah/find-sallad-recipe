import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('find_sallad_recipes')

ingredients_sheet = SHEET.worksheet('ingredients')
all_ingredients = ingredients_sheet.get_all_values()

print("Are you craving for some yummy sallad?")
print("Tell your favourite veggie, and I show you what you can make out of it.")
def ask_for_veggie():
    """
    Get user's favourite vegetable
    """
    while True:
        global favourite_veggie
        favourite_veggie_input = input("Type one vegetable. For example: tomato \n")
        favourite_veggie = favourite_veggie_input.lower()
        if validate_favourite_veggie(favourite_veggie):
            print ("I am looking for recipes..")
            break
        return favourite_veggie

def validate_favourite_veggie(veggie):
    try:
        if veggie.isnumeric():
            raise ValueError
    except ValueError as e:
        print("Please type a vegtable") 
        return False
    return True

def get_columns():
    """
    Makes the columns list
    """
    all_columns=[]
    for columns_index in range(len(all_ingredients[0])):
        columns = [row[columns_index] for row in all_ingredients]
        all_columns.append(columns)
    #print(all_columns)
    return(all_columns)


def find_matching_recipe(veggie, columns):
    """
    Find recipes, which contain the input ingredient.
    """
    for ingredient in columns:
        if veggie in ingredient:
            print("Hurray, I show you your match!")
            show_matching_recipe(favourite_veggie, get_columns())
            break 
        else:
            print("Oh no, I haven't found any recipes, try it again with something else.")
        all_functions()
    
def show_matching_recipe(veggie, columns):
    """ 
    Delete empty objects from list, then shows which list has the favorite_veggie ingredient.
    """
    spaceless_columns=[]
    for column in columns:
        spaceless_column=[]
        for x in column:
            if x.strip() != '':
                spaceless_column.append(x)
        spaceless_columns.append(spaceless_column)
        
   
    for index, column in enumerate(spaceless_columns):
        #print(f"index {index} : {column}")
        num_list = f"{index} : {column}"
        #print(num_list)
        if veggie in num_list:
            print(f"Name: {column[0]}. Other ingredients: {column[1:]}")
            

def all_functions():
    """
    Plays the whole sequence.
    """
    ask_for_veggie()
    get_columns()
    find_matching_recipe(favourite_veggie, get_columns())
    #show_matching_recipe(favourite_veggie, get_columns())
    

all_functions()


