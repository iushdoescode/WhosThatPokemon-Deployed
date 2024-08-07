import streamlit as st
from PIL import Image
import matplotlib.pyplot as plt
import tensorflow as tf
import numpy as np
import pandas as pd
from tensorflow import keras
from tensorflow.keras.models import load_model
from tensorflow.keras import preprocessing
import time
import requests #test commit
st.set_page_config(
    page_title='''WHO'S THAT POKEMON''',
    page_icon='827ed6bc234ff07054502083a9a2eb7c.jpg'
)
fig = plt.figure()
st.image('Whos-that-Pokemon.png', width=400)

class_names = ['Abra',
               'Aerodactyl',
               'Alakazam',
               'Alolan Sandslash',
               'Arbok',
               'Arcanine',
               'Articuno',
               'Beedrill',
               'Bellsprout',
               'Blastoise',
               'Bulbasaur',
               'Butterfree',
               'Caterpie',
               'Chansey',
               'Charizard',
               'Charmander',
               'Charmeleon',
               'Clefable',
               'Clefairy',
               'Cloyster',
               'Cubone',
               'Dewgong',
               'Diglett',
               'Ditto',
               'Dodrio',
               'Doduo',
               'Dragonair',
               'Dragonite',
               'Dratini',
               'Drowzee',
               'Dugtrio',
               'Eevee',
               'Ekans',
               'Electabuzz',
               'Electrode',
               'Exeggcute',
               'Exeggutor',
               'Farfetchd',
               'Fearow',
               'Flareon',
               'Gastly',
               'Gengar',
               'Geodude',
               'Gloom',
               'Golbat',
               'Goldeen',
               'Golduck',
               'Golem',
               'Graveler',
               'Grimer',
               'Growlithe',
               'Gyarados',
               'Haunter',
               'Hitmonchan',
               'Hitmonlee',
               'Horsea',
               'Hypno',
               'Ivysaur',
               'Jigglypuff',
               'Jolteon',
               'Jynx',
               'Kabuto',
               'Kabutops',
               'Kadabra',
               'Kakuna',
               'Kangaskhan',
               'Kingler',
               'Koffing',
               'Krabby',
               'Lapras',
               'Lickitung',
               'Machamp',
               'Machoke',
               'Machop',
               'Magikarp',
               'Magmar',
               'Magnemite',
               'Magneton',
               'Mankey',
               'Marowak',
               'Meowth',
               'Metapod',
               'Mew',
               'Mewtwo',
               'Moltres',
               'MrMime',
               'Muk',
               'Nidoking',
               'Nidoqueen',
               'Nidorina',
               'Nidorino',
               'Ninetales',
               'Oddish',
               'Omanyte',
               'Omastar',
               'Onix',
               'Paras',
               'Parasect',
               'Persian',
               'Pidgeot',
               'Pidgeotto',
               'Pidgey',
               'Pikachu',
               'Pinsir',
               'Poliwag',
               'Poliwhirl',
               'Poliwrath',
               'Ponyta',
               'Porygon',
               'Primeape',
               'Psyduck',
               'Raichu',
               'Rapidash',
               'Raticate',
               'Rattata',
               'Rhydon',
               'Rhyhorn',
               'Sandshrew',
               'Sandslash',
               'Scyther',
               'Seadra',
               'Seaking',
               'Seel',
               'Shellder',
               'Slowbro',
               'Slowpoke',
               'Snorlax',
               'Spearow',
               'Squirtle',
               'Starmie',
               'Staryu',
               'Tangela',
               'Tauros',
               'Tentacool',
               'Tentacruel',
               'Vaporeon',
               'Venomoth',
               'Venonat',
               'Venusaur',
               'Victreebel',
               'Vileplume',
               'Voltorb',
               'Vulpix',
               'Wartortle',
               'Weedle',
               'Weepinbell',
               'Weezing',
               'Wigglytuff',
               'Zapdos',
               'Zubat']

st.title('''Gotta catch 'em all..!!''')

st.markdown(
    '''- This tool will help you identify :the Pokemon you encounter in your way in the **Kanto Region** *(GEN 1).*
- Just upload an image of a GEN 1 pokemon to see which Pokemon it is.'''
)




def main():

    file_uploaded = st.file_uploader(
        "Choose File", type=["png", "jpg", "jpeg"])
    class_btn = st.button("CLASSIFY!!")
    if file_uploaded is not None:
        image = Image.open(file_uploaded)
        st.image(image, caption='Uploaded Image', use_column_width=True)

    if class_btn:
        if file_uploaded is None:
            st.write("Invalid command, please upload an image")
        else:
            with st.spinner('Wait For a sec.....'):
                predictions = predict(image)
                time.sleep(1)
                st.success('Gotcha your pokemon was found')
                print_data1(predictions)
def path_to_image_html(path):
    return '<img src="'+ path + '" width="60" >'

def predict(image):
    IMAGE_SHAPE = (128, 128, 3)
    model = load_model("model_pokemon.h5")
    test_image = image.convert("RGB").resize((128, 128))
    test_image = np.array(test_image)
    test_image = test_image / 255.0
    img_array = tf.expand_dims(test_image, 0)

    predictions = model.predict(img_array)
    scores = tf.nn.softmax(predictions[0])
    scores = scores.numpy()
    highest = scores.argsort()[-5:][::-1]
    result = [class_names[highest[0]]]
    # for i in range(1):
    #     result.append(class_names[highest[i]])
    #     i += 1
    return result
def print_data1(pokelist):
    url = 'https://pokeapi.co/api/v2/pokemon/'
    df = pd.DataFrame(data=np.zeros((1, 4)),
                      columns=['Name',  'Type', 'Description', 'Image'],
                      index=np.linspace(1, 1, 1, dtype=int)
                      )    
    sprites_path = 'https://github.com/iushdoescode/WhosThatPokemon-Deployed/blob/master/Sprites/'
    sprites = []
    i = 0
    for poke in pokelist:
        response = requests.get(url+poke.lower())
        if(response.status_code != 200):

            df.iloc[i, 0] = poke
            df.iloc[i, 1] = 'Error fetching data from API'
            df.iloc[i, 2] = 'Error fetching data from API'
            sprites.append(sprites_path+'0.png?raw=true')

        else:
            jresponse = response.json()
            type = jresponse['types'][0]['type']['name']
            id = jresponse['id']
            species_url = jresponse['species']['url']
            species_response = requests.get(species_url)
            species_response = species_response.json()
            description = ''
            for d in species_response['flavor_text_entries']:
                if d['language']['name'] == 'en':
                    description = d['flavor_text']
                    break
            df.iloc[i, 0] = poke.capitalize()
            df.iloc[i, 1] = type.capitalize()
            description = description.replace('\n', ' ')
            description = description.replace('', ' ')
            df.iloc[i, 2] = description
            sprites.append(sprites_path+str(id)+'.png?raw=true')
    
    i += 1
    df['Image'] = sprites
    st.title("Your Pokemon is Most Likely")   
    st.write(df.to_html(escape=False, formatters=dict(Image=path_to_image_html)), unsafe_allow_html=True)
# def print_data2(pokelist):
#     url = 'https://pokeapi.co/api/v2/pokemon/'
#     df2=pd.DataFrame(data=np.zeros((4, 4)),
#                      columns=['Name',  'Type', 'Description', 'Image'],
#                      index=np.linspace(1, 4, 4, dtype=int)
#                       )
    
#     sprites_path = 'https://github.com/iushdoescode/WhosThatPokemon-Deployed/blob/master/Sprites/'
#     sprites = []

#     j=0
#     for poke in pokelist:
#         response = requests.get(url+poke.lower())
#         if(response.status_code != 200):

#             df2.iloc[j, 0] = poke
#             df2.iloc[j, 1] = 'Error fetching data from API'
#             df2.iloc[j, 2] = 'Error fetching data from API'
#             sprites.append(sprites_path+'0.png?raw=true')

#         else:
#             jresponse = response.json()
#             type = jresponse['types'][0]['type']['name']
#             id = jresponse['id']
#             species_url = jresponse['species']['url']
#             species_response = requests.get(species_url)
#             species_response = species_response.json()
#             description = ''
#             for d in species_response['flavor_text_entries']:
#                 if d['language']['name'] == 'en':
#                     description = d['flavor_text']
#                     break
#             df2.iloc[j, 0] = poke.capitalize()
#             df2.iloc[j, 1] = type.capitalize()
#             description = description.replace('\n', ' ')
#             description = description.replace('', ' ')
#             df2.iloc[j, 2] = description
#             sprites.append(sprites_path+str(id)+'.png?raw=true')
    
#     j += 1
#     df2['Image'] = sprites
#     st.title("But Your Pokemon can Also Be...")   
#     st.write(df2.to_html(escape=False, formatters=dict(Image=path_to_image_html)), unsafe_allow_html=True)


if __name__ == "__main__":
    main()
