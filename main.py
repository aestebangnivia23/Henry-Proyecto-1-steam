from fastapi import FastAPI
import pandas as pd
import gdown

url = "https://drive.google.com/uc?id=ID_DE_TU_ARCHIVO"
output = "./data/recomendacion_juego.parquet"
gdown.download(url, output, quiet=False)


app = FastAPI()

df_user_for_genre = pd.read_csv('./data/UserForGenre.csv')
df_play_time_genre = pd.read_csv('./data/PlayTimeGenre.csv')
df_user_recommend = pd.read_csv('./data/UserRecommend.csv')
df_user_not_recommend = pd.read_csv('./data/UserNotRecommend.csv')
df_sentiment_analysis = pd.read_csv('./data/sentiment_analysis.csv')
df_recomendacion_juego = pd.read_parquet('./data/recomendacion_juego.parquet')
df_recomendacion_juego.set_index('id',inplace=True)

@app.get('/PlayTimeGenre/{genre}', name='Ingrese el genero para el que desea conocer el año con mas horas de juego')
def PlayTimeGenre(genero: str = 'Action')-> dict:
    
    """
    Retrieves the year with the most cumulative playtime for a specified genre.

    Args:
        genero (str, optional): The genre for which the year with the most cumulative playtime is searched. Defaults to 'Action'.

    Returns:
        dict: A dictionary containing JSON data with the year that had the most cumulative playtime for the specified genre.
    """
    
    df_filtered_by_genre_playtime = df_play_time_genre[df_play_time_genre['genre'] == genero.lower()]
    top_year = int(df_filtered_by_genre_playtime.top_year.iloc[0])

    return {'Año de lanzamiento con más horas jugadas para {}'.format(genero): top_year}

@app.get('/UserForGenre/{genre}', name='Ingrese el genero para el cual desea conocer el jugador con mas horas de juego y el listado de horas jugadas por año')
def UserForGenre(genero: str = 'Action')-> dict:
    
    """
    Retrieves the user who has played the most hours in a given genre, along with their hours played per year.

    Args:
        genero (str, optional): The genre for which the user with the most hours played is searched. Defaults to 'Action'.

    Returns:
        dict: A dictionary containing JSON data about the user with the most hours played in the specified genre.
              The dictionary includes the user's ID, and a list of hours played per year.
    """
    
    df_filtered_by_genre_user = df_user_for_genre[df_user_for_genre['genre'] == genero.lower()]
    hours_year_list = [
        {'Año':year, 'Horas':hours} for year, hours in zip(df_filtered_by_genre_user['year'],df_filtered_by_genre_user['playtime_forever']) 
    ]

    result= {
        'Usuario con mas horas jugadas por genero {}'.format(genero): df_filtered_by_genre_user.top_user_id.iloc[0],
        'Horas jugadas': hours_year_list
        }


    return result 


@app.get('/UsersRecommend/{year}', name='Ingrese el año para el cual desea conocer los 3 juegos mas recomendados')
def UsersRecommend(año: int = 2014)-> list:
    
    """
    Gets the top 3 games recommended for a given year.

    Args:
        año (int, optional): The year for which the top 3 games are searched. Defaults to 2014.

    Returns:
        list: A list containing JSON data about the top 3 games recommended for the specified year.
              Each entry in the list contains a dictionary with the game name and its ranking. 
    """
    
    df_filtered_by_year = df_user_recommend[df_user_recommend['year'] == año]

    return [{"Puesto 1" : df_filtered_by_year.iloc[0].app_name}, 
            {"Puesto 2" : df_filtered_by_year.iloc[1].app_name},
            {"Puesto 3" : df_filtered_by_year.iloc[2].app_name}]

@app.get('/UsersNotRecommend/{year}', name='Ingrese el año para el cual desea conocer los 3 juegos menos recomendados')
def UsersNotRecommend(año: int = 2014)-> list:
    
    """
    Gets the top 3 games not recommended for a given year.

    Args:
        año (int, optional): The year for which the top 3 games are searched. Defaults to 2014.

    Returns:
        list: A list containing JSON data about the top 3 games not recommended for the specified year.
              Each entry in the list contains a dictionary with the game name and its ranking."""
    
    df_filtered_by_year = df_user_not_recommend[df_user_not_recommend['year'] == año]

    return [{"Puesto 1" : df_filtered_by_year.iloc[0].app_name}, 
            {"Puesto 2" : df_filtered_by_year.iloc[1].app_name},
            {"Puesto 3" : df_filtered_by_year.iloc[2].app_name}]


@app.get('/sentiment_analysis/{year}', name='Ingrese el año para el cual desea conocer la cantidad de juegos que tuvieron reseñas positivas, negativas y neutras')
def sentiment_analysis(año: int = 2014)-> dict:
    
    """
    Retrieves sentiment analysis data for a specified year.

    Args:
        año (int, optional): The year for which sentiment analysis data is retrieved. Defaults to 2014.

    Returns:
        dict: A dictionary containing JSON data with the count of negative, neutral, and positive sentiments for the specified year.
    """
    
    df_filtered_by_year = df_sentiment_analysis[df_sentiment_analysis['year'] == año]

    return {'Negative': int(df_filtered_by_year['conteo'].iloc[0]), 
            'Neutral' : int(df_filtered_by_year['conteo'].iloc[1]),
            'Positive' : int(df_filtered_by_year['conteo'].iloc[2])}


@app.get('/recomendacion_juego', name='Ingrese el id del juego para el cual desea 5 recomendaciones')
def recomendacion_juego(id_juego: str = '10090')-> dict:
    """
    Retrieves the top game recommendations for a given game ID.

    Args:
        id_juego (str, optional): The ID of the game for which recommendations are retrieved. Defaults to '10090'.

    Returns:
        dict: A dictionary containing JSON data with the top game recommendations for the specified game ID.
    """
    
    
    df_recomendacion_juego_filtered_by_id = df_recomendacion_juego.loc[:,id_juego].sort_values(ascending = False)
    games_recommended_id = list(df_recomendacion_juego_filtered_by_id.index[:6])
    games_recommended_id.remove(int(id_juego))
    list_games_recommended = list(df_recomendacion_juego[df_recomendacion_juego.index.isin(games_recommended_id)].app_name)

    return {id_juego: list_games_recommended}
