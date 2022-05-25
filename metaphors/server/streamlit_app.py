import streamlit as st

from metaphors.applications.bionic_reading.server.streamlit import BionicReadingApp


def app():
    application = st.sidebar.selectbox("Select the application", ["BionicReading"])

    if application == "BionicReading":
        BionicReadingApp().start()
    else:
        pass


if __name__ == "__main__":
    app()
