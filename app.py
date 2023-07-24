import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st


@st.cache_data
def update_transmission_df(df, d):
    return df.applymap(lambda x: np.exp(-x * d))


@st.cache_data
def calculate_pa_df(mcl_df, transmission_df):
    return transmission_df * mcl_df


def main():
    st.title("Simulation")

    # Create a sidebar to accept the file path
    st.sidebar.title("Upload Excel File")
    mcl_data = st.sidebar.file_uploader("Upload the MCL data excel file", type=["xlsx"])

    if mcl_data is not None:
        # Load DataFrame from the uploaded CSV file
        mcl_df = pd.read_excel(mcl_data)
        container = st.container()
        l, r = container.columns([0.5, 0.5])

        mcl_df.set_index("Wavelength (nm)", inplace=True)

        # Display the DataFrame
        l.subheader("MCL Data:")
        l.dataframe(mcl_df)

        # fig = plt.figure()
        # ax = fig.add_subplot(1, 1, 1)

        fig, ax = plt.subplots()

        mcl_df.plot(ax=ax)
        r.subheader("Absorbance")
        r.pyplot(fig)

        columns = st.sidebar.multiselect("Columns", mcl_df.columns)
        if len(columns) > 0:
            distance = st.sidebar.slider(
                "Distance (mm)", value=1, min_value=1, max_value=20
            )
            d = distance * 1e-3

            container = st.container()
            l, r = container.columns([0.5, 0.5])

            transmission_df = update_transmission_df(mcl_df[columns], d)

            # fig2 = plt.figure()
            # ax2 = fig2.add_subplot(1, 1, 1)
            fig, ax = plt.subplots()
            ax.set_ylim(
                np.exp(-mcl_df.max().max() * 20e-3), np.exp(-mcl_df.min().min() * 20e-3)
            )

            transmission_df.plot(ax=ax)
            l.subheader("Transmission")
            if l.checkbox("Override legend?", key="transmission_legend_checkbox"):
                custom_column_names = [
                    l.text_input(
                        f"{column} -> ", key=f"transmission_legend_input_{column}"
                    )
                    for column in (columns)
                ]
                ax.legend(custom_column_names)
            l.pyplot(fig)
            fig, ax = plt.subplots()
            # pa_df = pd.DataFrame(index=mcl_df.index)
            pa_df = calculate_pa_df(mcl_df[columns], transmission_df)
            ax.set_ylim(mcl_df.min().min(), mcl_df.max().max())
            pa_df.plot(ax=ax)
            r.subheader("PA Signal")
            if r.checkbox("Override legend?", key="pa_signal_legend_checkbox"):
                custom_column_names = [
                    r.text_input(
                        f"{column} -> ", key=f"pa_signal_legend_input_{column}"
                    )
                    for column in (columns)
                ]
                ax.legend(custom_column_names)
            r.pyplot(fig)


if __name__ == "__main__":
    main()
