import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import pickle
import base64

# Load the saved recommendation model
with open('rrs_model1.pkl', 'rb') as file:
    saved_data = pickle.load(file)

tfidf_matrix = saved_data['tfidf_matrix']
cosine_similarities = saved_data['cosine_similarities']
df = saved_data['df']
indices = saved_data['indices']

# Define the recommend function
def recommend(name):
    # Find the index of the restaurant entered
    idx = indices[indices == name].index[0]

    # Find the restaurants with a similar cosine-sim value and order them
    score_series = pd.Series(cosine_similarities[idx]).sort_values(ascending=False)

    # Extract top 30 restaurant indexes with similar cosine-sim value
    top30_indexes = list(score_series.iloc[0:31].index)

    # Names of the top 30 restaurants
    recommend_restaurants = []
    for each in top30_indexes:
        recommend_restaurants.append(list(df.index)[each])

    # Creating the new data set to show similar restaurants
    df_new = pd.DataFrame(columns=['Cuisines', 'Mean Rating', 'Cost', 'Timings'])

    # Create the top 30 similar restaurants with some of their columns
    for each in recommend_restaurants:
        df_new = pd.concat([df_new, df[['Cuisines', 'Mean Rating', 'Cost', 'Timings']][df.index == each].sample()])

    # Drop the same named restaurants and sort only the top 10 by the highest rating
    df_new = df_new.drop_duplicates(subset=['Cuisines', 'Mean Rating', 'Cost'], keep=False)
    df_new = df_new.sort_values(by='Mean Rating', ascending=False).head(10)

    return df_new

# Streamlit app

#Add an image from local
def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"jpg"};base64,{encoded_string.decode()});
        background-size: cover;
        background-repeat: no-repeat;
        background-position: center;
        font-weight: bold !important;
        color: white;  
        font-family: 'Arial', sans-serif; 
         
        
    }}
   
    </style>
    """,
    unsafe_allow_html=True
    )
add_bg_from_local(r"D:\Feynn Labs\golden-cutlery-with-textile-plate-dark-background-top-view.jpg")

# def main():   
#     # giving a title
    
#     st.markdown("""
#     <style>
#     .big-font {
#         font-size:70px !important;
#     }
         
#     </style>
#     """, unsafe_allow_html=True)
    
#     st.markdown('<p class="big-font">Restaurant Recommendation App </p>', unsafe_allow_html=True)
#   css-10trblm e16nr0p30

def main():
    st.markdown(
        """
        <style>
        h1 {
            font-size: 45px !important;
            font-weight: bold !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.title("Restaurant Recommendation App")

    # Add css to make text bigger
    # st.markdown(
    #     """
    #     <style>
    #     textarea {
    #         font-size: 0.5rem !important;
    #     }
    #     input {
    #         font-size: 1rem !important;
    #     }
    #     .css-q8sbsg  {
    #         font-size: 20px;
    #     }
    #     .css-q8sbsg {
    #         font-weight: bold;
    #     }
    #     </style>
    #     """,
    #     unsafe_allow_html=True,
    # )

    # Get unique sorted restaurant names
    restaurant_names = sorted(df.index.unique())

    # Input for restaurant name

    label_text = "<span style='font-size: 30px;'>Enter a restaurant name:</span>"
    st.markdown(label_text, unsafe_allow_html=True)
    restaurant_name = st.selectbox("", options=[""] + restaurant_names)

    # Check if restaurant name is selected
    if restaurant_name and restaurant_name != "":
        try:
            # Call the recommend function to get recommendations
            recommendations = recommend(restaurant_name)
            st.subheader(f"Top {len(recommendations)} restaurants similar to {restaurant_name}:")
            st.table(recommendations)

        except IndexError:
            st.error("Restaurant not found. Please select a valid restaurant name.")

# Run the Streamlit app
if __name__ == '__main__':
    main()

