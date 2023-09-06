from fastapi import FastAPI, Body
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from typing import Optional

class Movie(BaseModel):
    id: Optional[int]
    #id: int | None = None -> una foma de decir que sera nulo
    title: str = Field(min_length=20, max_length=128)
    overview: str = Field(min_length=128, max_length=256)
    year:int = Field(le=2023)
    rating: float 
    category: str 
    
    class Config: # -> clase que funciona como schema ejemplo dentro de la documentación
        schema_extra = {
            "example":{
                "id" : 1,
                "title" : "Mi película",
                "overview" : "Descipción de la película",
                "year" :  2023,
                "rating" : 9.9,
                "category" : "Acción"
            }
        }
        

app = FastAPI()

app.title = "API MOVIES" # titulo del /docs
app.version = "0.0.1" # Version de API /docs

movies = [
    {
        'id': 1,
        'title': 'Avatar',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': '2009',
        'rating': 7.8,
        'category': 'Acción'    
    },
    {
        'id': 2,
        'title': 'El origen',
        'overview': "Dom Cobb es un ladrón capaz de adentrarse en los sueños de la gente y hacerse con sus secretos. ...",
        'year': '2010',
        'rating': 9.8,
        'category': 'Suspenso'    
    },
]



@app.get('/', tags=['Home']) # Etiqueta para agrupar rutas
@app.get('/')
def menssage():
    return HTMLResponse('<h1>HELLO WORLD</h1>') # respuesta html


@app.get('/Movies', tags=['movies'])
def get_movies():
    return movies

#Filtrado de peliculas por ID -> elcual se indica en la URL
@app.get('/movies/{id}', tags=['movies'])
def get_movie(id : int ):
    for movie in movies:
        if movie["id"] == id:
            return movie
    return []

# Filtrado de categorías por Querys
@app.get('/movies/', tags=['movies'])
def get_movies_by_category(category : str):
    return [movie for movie in movies if movie['category']== category  ] # filtra las peliculas por categoría

"""
# Forma de crear un post sin Base model
@app.post('/movies/', tags=['movies'])
def create_movie (id: int = Body(), title: str = Body(), overview: str = Body(), year:int = Body(),
                  rating: float = Body(), category: str = Body() ):
    movies.append({
        'id': id,
        'title': title,
        'overview': overview,
        'year': year,
        'rating': rating,
        'category': category 
        })
    return movies
"""
#Con base Model
@app.post('/movies/', tags=['movies'])
def create_movie (movie : Movie ):
    movies.append(movie)
    return movies


""" 
@app.put('/movies/{id}', tags=['movies'])
def update_movie(id: int, title: str = Body(), overview: str = Body(), year:int = Body(),
                  rating: float = Body(), category: str = Body() ):
    for movie in movies:
        if movie['id'] == id:
            movie['title'] = title,
            movie['overview'] = overview,
            movie['year'] = year,
            movie['rating'] = rating,
            movie['category'] = category,
            return movies
"""       

@app.put('/movies/{id}', tags=['movies'])
def update_movie(id: int, movie : Movie):
    for item in movies:
        if item['id'] == id:
            item['title'] = movie.title
            item['overview'] = movie.overview
            item['year'] = movie.year
            item['rating'] = movie.rating
            item['category'] = movie.category
            return movies
        

@app.delete('/movies/{id}', tags=['movies'])
def delete_movie(id : int):
    for movie in movies:
        if movie['id'] == id:
            movies.remove(movie)
            return movies
