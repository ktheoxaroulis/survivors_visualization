from vega_datasets import data
import matplotlib.pyplot as plt
import streamlit as st
import altair as alt
import pandas as pd
from PIL import Image
import seaborn as sns

def main():
    df = load_data()
    ep_data = load_ep_data()

    page = st.sidebar.selectbox("Choose a page", ["Homepage", "Sociodemographic", "Exploration"])
    team_image = Image.open("images/image.png")
    corona_image = Image.open("images/corona.png")

    if page == "Homepage":
        st.header("Covid-19 Hackathon Greece")
        st.subheader("Team: Survivors")
        st.image(team_image, width=100)
        st.write("As we can see from the current facts, recovery from Covid-19 depends on several factors ( supportive care , patient’s response e.t.c ) and of course investigational treatments are currently increasing. \n \
                  \nThose who do or will recover probably will develop antibodies. It is not known yet if people who recover are immune for life or if they can later become infected with a different species of Covid virus. Some survivors may have long-term complications . \n \
                  \nThe idea was to create a simple app where those who were recovered will fill periodically a survey, tracking down several possible health issues \n \
                  \n Here you ll find the on-going results and the analysis of these data \n ")

    elif page == "Sociodemographic":
        st.header("Epidemiological Data")

        # Show Dataset
        if st.checkbox("Preview Data Frame"):
            st.write(ep_data.drop(['userId'], axis=1))

        charttable_dim = st.radio('What type of info would you like to see', ('tables', 'charts'))
        if charttable_dim == 'tables':
            st.header("Epidemiological Tables")

            age = ep_data['age'].values
            ageRange = pd.Series([])

            for i in range(len(ep_data)):
                if age[i] < 18:
                    ageRange[i] = '<18'
                elif age[i] >= 18 and age[i] <= 24:
                    ageRange[i] = '18-24'
                elif age[i] >= 25 and age[i] <= 34:
                    ageRange[i] = '25-34'
                elif age[i] >= 35 and age[i] <= 44:
                    ageRange[i] = '35-44'
                elif age[i] >= 45 and age[i] <= 54:
                    ageRange[i] = '45-54'
                elif age[i] >= 55 and age[i] <= 64:
                    ageRange[i] = '55-64'
                elif age[i] >= 65:
                    ageRange[i] = '>65'
                else:
                    ageRange[i] = 'Unknown'

            st.subheader("Age Summary")
            ep_data.insert(2, "ageRange", ageRange)
            counts = ep_data['ageRange'].value_counts()
            #percent = ep_data['ageRange'].value_counts(normalize=True)
            percent100 = ep_data['ageRange'].value_counts(normalize=True).mul(100).round(decimals=1).astype(str) + '%'
            ageSumm = pd.DataFrame({'#users': counts, '%Users': percent100})
            st.write(ageSumm.sort_values('%Users'))

            ## Gender Summary
            st.subheader("Gender Summary")

            gen_counts = ep_data['gender'].value_counts()
            gen_percent = ep_data['gender'].value_counts(normalize=True)
            gen_percent100 = ep_data['gender'].value_counts(normalize=True).mul(100).round(decimals=1).astype(str) + '%'
            genSumm = pd.DataFrame({'#users': gen_counts, '%Users': gen_percent100})
            st.write(genSumm.sort_values('%Users'))

            ## Marital Status Summary
            st.subheader("Marital Summary")

            mar_counts = ep_data['maritalStatus'].value_counts()
            mar_percent = ep_data['maritalStatus'].value_counts(normalize=True)
            mar_percent100 = ep_data['maritalStatus'].value_counts(normalize=True).mul(100).round(decimals=1).astype(
                str) + '%'
            marSumm = pd.DataFrame({'#users': mar_counts, '%Users': mar_percent100})
            st.write(marSumm.sort_values('%Users'))

            ## Employee Status Summary
            st.subheader("Employee Status Summary")

            emp_counts = ep_data['employment'].value_counts()
            emp_percent = ep_data['employment'].value_counts(normalize=True)
            emp_percent100 = ep_data['employment'].value_counts(normalize=True).mul(100).round(decimals=1).astype(str) + '%'
            empSumm = pd.DataFrame({'#users': emp_counts, '%Users': emp_percent100})
            st.write(empSumm.sort_values('%Users'))

        elif charttable_dim == 'charts':
            st.header("Epidemiological Charts")
            data_dim = st.radio('What type of plots do you want to show', ('bars', 'histograms'))
            if data_dim == 'bars':
                ######## Static predifined  ###
                sns.set(font_scale=1.4)
                ep_data['gender'].value_counts().plot(kind='bar', figsize=(14, 3), rot=0)
                plt.xlabel("Gender", labelpad=14)
                plt.ylabel("Count of People", labelpad=14)
                plt.title("Count of People Who Recovered by Gender", y=1.02)
                st.pyplot()

                ######## Dynamic ###
                st.subheader("Dynamic Bar Plots")
                x_axis = st.selectbox("Choose a variable for the x-axis in order to count values", ep_data.columns, index=3)
                visualize_descriptive(ep_data, x_axis)



    elif page == "Exploration":
        st.title("Data Exploration")
        st.image(corona_image, width =100)
        x_axis = st.selectbox("Choose a variable for the x-axis", df.columns, index=3)
        y_axis = st.selectbox("Choose a variable for the y-axis", df.columns, index=4)
        visualize_data(df, x_axis, y_axis)

@st.cache
def load_data():
    df = data.cars()
    return df
def load_ep_data():
    ep_data = pd.read_csv("data/epidemiological.csv")
    return ep_data

def visualize_descriptive(df, x_axis):
    graph = alt.Chart(df).mark_bar().encode(
        x=x_axis,
        y='count()',
        color=x_axis,
    ).interactive()
    st.write(graph)

def visualize_data(df, x_axis, y_axis):
    graph = alt.Chart(df).mark_circle(size=60).encode(
        x=x_axis,
        y=y_axis,
        color='Origin',
        tooltip=['Name', 'Origin', 'Horsepower', 'Miles_per_Gallon']
    ).interactive()
    st.write(graph)

if __name__ == "__main__":
    main()

