import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image
from streamlit_folium import folium_static
import folium
import random

# Title of the web app
st.title('Rotten World')

# Description of the web app
st.write('Welcome to Rotten World! This is a simple web app that uses a TensorFlow ML Model to predict the freshness of a fruit. To get started, upload an image of the fruit below.')

# Load the model
@st.cache_resource
def load_model():
    model = tf.keras.models.load_model('model.h5')
    return model

# Load the model and show a loading spinner while loading the model
with st.spinner("Loading Model...."):
    model = load_model()


def predict_class(image, model):

	image = tf.cast(image, tf.float32)
	image = tf.image.resize(image, [442, 368])

	image = np.expand_dims(image, axis = 0)

	prediction = model.predict(image)

	return prediction

image = st.file_uploader('Upload Image', type=['jpg', 'png', 'jpeg'])

if image is not None:
    st.write("Predicting Class...")
    with st.spinner("Classifying..."):
        slot = st.empty()
        test_image = Image.open(image)
        st.image(test_image, caption="Input Image", width = 400)
        pred = predict_class(np.asarray(test_image), model)
        class_names = ['Fresh Apples', 'Fresh Banana', 'Fresh Oranges', 'Rotten Apples', 'Rotten Banana', 'Rotten Oranges']
        result = class_names[np.argmax(pred)]
        confidence = str(round(100 * np.max(pred), 2))
        output = 'The image is a ' + result + ' with a confidence of ' + confidence + '%'

        output2 = ''

        if (confidence<'39'):
            output = 'I could not recognize this🤔'
            output2 = 'Please upload a clear image'
        else:
            if (result=='Fresh Apples' and confidence > '85'):
                output2 = 'The apple is good to eat for more 5-7 days'
            elif (result=='Fresh Banana' and confidence > '85'):
                output2 = 'The banana is good to consume within 4 days'
            elif (result=='Fresh Oranges' and confidence > '85'):
                output2 = 'The orange is good to consume within 7 days'
        

            elif (result=='Fresh Apples' and confidence > '65'):
                output2 = 'The apple is good to eat for more 2-3 days'
            elif (result=='Fresh Banana' and confidence > '65'):
                output2 = 'The banana is good to consume within 2 days'
            elif (result=='Fresh Oranges' and confidence > '65'):
                output2 = 'The orange is good to consume within 2 days'

            elif (result=='Fresh Apples' and confidence < '50'):
                output2 = 'Consume it within 1 day'
            elif (result=='Fresh Banana' and confidence <'50'):
                output2 = 'Consume it within 1 day'
            elif (result=='Fresh Oranges' and confidence > '50'):
                output2 = 'Consume it within 1 day'
        
            elif (result=='Rotten Apples'):
                output2 = 'Throw it away'
            elif (result=='Rotten Banana'):
                output2 = 'Throw'
            elif (result=='Rotten Oranges'):
                output2 = 'Throw'

        
        
        

        
        
        slot.text('Done')
        st.success(output)
        st.success(output2)
        
else:
    st.warning('Please upload an image.')

# Function to generate random points around McMaster University
def generate_random_points(center, num_points):
    random_points = []
    for _ in range(num_points):
        # Adding random offsets to latitude and longitude
        offset_lat = random.uniform(-0.03, 0.03)
        offset_lon = random.uniform(-0.03, 0.03)
        random_point = (center[0] + offset_lat, center[1] + offset_lon)
        random_points.append(random_point)
    return random_points

# McMaster University coordinates
hamilton_coords = (43.25011000, -79.84963000)

# Number of random points to generate
num_random_points = 6

# Streamlit app
st.title('')

# Generate random points around McMaster University
random_points = generate_random_points(hamilton_coords, num_random_points)

# Display map using folium
map_center = hamilton_coords
mymap = folium.Map(location=map_center, zoom_start=12)

# Add markers for McMaster University and random points
folium.Marker(location=hamilton_coords, popup='McMaster University', icon=folium.Icon(color='blue')).add_to(mymap)
folium.Marker(location=random.choice(random_points), popup=folium.Popup(f'McNGO\n 5 Apples\n Consume within 5 days', max_width=50), icon=folium.Icon(color='green')).add_to(mymap)
folium.Marker(location=random.choice(random_points), popup=folium.Popup(f'MnMNGO\n 10 Bananas\n Consume within 3 days', max_width=50), icon=folium.Icon(color='green')).add_to(mymap)
folium.Marker(location=random.choice(random_points), popup=folium.Popup(f'HgNGO\n 3 Oranges\n Consume within 6 days', max_width=50), icon=folium.Icon(color='green')).add_to(mymap)
folium.Marker(location=random.choice(random_points), popup=folium.Popup(f'BcNGO\n 2 Bananas\n Consume within 2 days', max_width=50), icon=folium.Icon(color='green')).add_to(mymap)
folium.Marker(location=random.choice(random_points), popup=folium.Popup(f'McNGO\n 2 Apples\n Consume within 4 days', max_width=50), icon=folium.Icon(color='green')).add_to(mymap)
folium.Marker(location=random.choice(random_points), popup=folium.Popup(f'TcNGO\n 6 Oranges\n Consume within 7 days', max_width=50), icon=folium.Icon(color='green')).add_to(mymap)


# Display the map using Streamlit
folium_static(mymap)
