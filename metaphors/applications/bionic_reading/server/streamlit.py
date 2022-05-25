import streamlit as st

from metaphors.applications.bionic_reading import BionicReading
from metaphors.applications.bionic_reading.settings import StopWordsBehavior, RareBehavior


class BionicReadingApp:
    """The BionicReadingApp class is a Python class that represents a Bionic Reading application"""

    def __init__(self):
        pass

    @staticmethod
    def start():
        """
        It creates a function that takes in the text and returns the text with the bionic reading features.
        """
        st.title("Bionic Reading")
        fixation = st.slider("fixation strength", min_value=0.0, max_value=1.0, value=0.7)
        saccades = st.slider("saccades strength", min_value=0.0, max_value=1.0, value=0.7)
        opacity = st.slider("opacity strength", min_value=0.0, max_value=1.0, value=0.7)
        stopwords = st.slider("stopwords strength", min_value=0.0, max_value=1.0, value=0.7)
        stopwords_behavior = st.selectbox(
            "stopwords_behavior", [behavior.value.lower() for behavior in StopWordsBehavior]
        )
        rare_words_behavior = st.selectbox("rare_words_behavior", [behavior.value.lower() for behavior in RareBehavior])
        rare_words_max_freq = st.slider("rare_words_max_freq", min_value=0, max_value=100)
        text = st.text_area("Enter the text here:")
        if text:
            _ = BionicReading(
                fixation=fixation,
                saccades=saccades,
                opacity=opacity,
                stopwords=stopwords,
                stopwords_behavior=stopwords_behavior,
                output_format="html",
                rare_words_behavior=rare_words_behavior,
                rare_words_max_freq=rare_words_max_freq,
            ).read_faster(text=text)
            st.markdown(_, unsafe_allow_html=True)
