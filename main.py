from fastapi import FastAPI
import pandas as pd
import gdown

# URL con el formato adecuado para gdown
url = "https://drive.google.com/uc?id=17bNn9xjxHFwXDPRRlou96Lkq5dJhcQdO"
output = './data/recomendacion_juego.parquet'

# Descargamos el archivo
gdown.download(url, output, quiet=False)

app = FastAPI()

# Carga de datos
df_user_for_genre = pd.read_csv('./data/UserForGenre.csv')
df_play_time_genre = pd.read_csv('./data/PlayTimeGenre.csv')
df_user_recommend = pd.read_csv('./data/UserRecommend.csv')
df_user_not_recommend = pd.read_csv('./data/UserNotRecommend.csv')
df_sentiment_analysis = pd.read_csv('./data/sentiment_analysis.csv')
df_recomendacion_juego = pd.read_parquet('./data/recomendacion_juego.parquet')
df_recomendacion_juego.set_index('id', inplace=True)

@app.get("/")
def read_root():
    return {"message": "API is working!"}

@app.get('/PlayTimeGenre/{genre}', name='Ingrese el genero para el que desea conocer el año con mas horas de juego')
def PlayTimeGenre(genero: str = 'Action')-> dict:
    df_filtered_by_genre_playtime = df_play_time_genre[df_play_time_genre['genre'] == genero.lower()]
    top_year = int(df_filtered_by_genre_playtime.top_year.iloc[0])
    return {'Año de lanzamiento con más horas jugadas para {}'.format(genero): top_year}

@app.get('/UserForGenre/{genre}', name='Ingrese el genero para el cual desea conocer el jugador con mas horas de juego y el listado de horas jugadas por año')
def UserForGenre(genero: str = 'Action')-> dict:
    df_filtered_by_genre_user = df_user_for_genre[df_user_for_genre['genre'] == genero.lower()]
    hours_year_list = [{'Año': year, 'Horas': hours} for year, hours in zip(df_filtered_by_genre_user['year'], df_filtered_by_genre_user['playtime_forever'])]
    return {
        'Usuario con mas horas jugadas por genero {}'.format(genero): df_filtered_by_genre_user.top_user_id.iloc[0],
        'Horas jugadas': hours_year_list
    }

@app.get('/UsersRecommend/{year}', name='Ingrese el año para el cual desea conocer los 3 juegos mas recomendados')
def UsersRecommend(año: int = 2014)-> list:
    df_filtered_by_year = df_user_recommend[df_user_recommend['year'] == año]
    return [{"Puesto 1": df_filtered_by_year.iloc[0].app_name}, 
            {"Puesto 2": df_filtered_by_year.iloc[1].app_name},
            {"Puesto 3": df_filtered_by_year.iloc[2].app_name}]

@app.get('/UsersNotRecommend/{year}', name='Ingrese el año para el cual desea conocer los 3 juegos menos recomendados')
def UsersNotRecommend(año: int = 2014)-> list:
    df_filtered_by_year = df_user_not_recommend[df_user_not_recommend['year'] == año]
    return [{"Puesto 1": df_filtered_by_year.iloc[0].app_name}, 
            {"Puesto 2": df_filtered_by_year.iloc[1].app_name},
            {"Puesto 3": df_filtered_by_year.iloc[2].app_name}]

@app.get('/sentiment_analysis/{year}', name='Ingrese el año para el cual desea conocer la cantidad de juegos que tuvieron reseñas positivas, negativas y neutras')
def sentiment_analysis(año: int = 2014)-> dict:
    df_filtered_by_year = df_sentiment_analysis[df_sentiment_analysis['year'] == año]
    return {
        'Negative': int(df_filtered_by_year['conteo'].iloc[0]), 
        'Neutral': int(df_filtered_by_year['conteo'].iloc[1]),
        'Positive': int(df_filtered_by_year['conteo'].iloc[2])
    }

@app.get('/recomendacion_juego', name='Ingrese el id del juego para el cual desea 5 recomendaciones')
def recomendacion_juego(id_juego: str = '10090')-> dict:
    df_recomendacion_juego_filtered_by_id = df_recomendacion_juego.loc[:, id_juego].sort_values(ascending=False)
    games_recommended_id = list(df_recomendacion_juego_filtered_by_id.index[:6])
    games_recommended_id.remove(int(id_juego))
    list_games_recommended = list(df_recomendacion_juego[df_recomendacion_juego.index.isin(games_recommended_id)].app_name)
    return {id_juego: list_games_recommended}
