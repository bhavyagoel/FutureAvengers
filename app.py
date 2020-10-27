import json
from datetime import date
import sys

if sys.version_info >= (3, 8):
    import zipfile
else:
    import zipfile38 as zipfile
import streamlit as st
import os
from fbprophet.serialize import model_from_json


# import warnings
# warnings.simplefilter('ignore')


def welcome():
    return "Welcome All"


def future_predict(station, pollutant, fut_date):
    cur_date = date.today()
    delta = fut_date - cur_date
    num_days = delta.days
    archive = zipfile.ZipFile('models.zip', 'r')
    name = "models/" + str(pollutant) + "_" + str(station) + ".json"
    json_file = archive.open(name)
    # with open(name, 'r') as fin:
    #     m = model_from_json(json.load(fin))
    m = model_from_json(json.load(json_file))
    future = m.make_future_dataframe(periods=num_days, freq='D', include_history=True)
    forecast = m.predict(future)
    archive.close()
    json_file.close()
    return forecast.iloc[-1, -1]


def main():
    # st.beta_set_page_config("Avengers")
    st.title("@FutureAvengers")

    html_temp = """
    <div style="background-color:skyblue;padding:10px">
    <h1 style="color:white;text-align:center;"><em>Future Risk Predicition</em></h1>
    </div>
    <br></br>
    """

    st.markdown(html_temp, unsafe_allow_html=True)

    st.write("""
    # Procedure to use this App:
    ### Input the following:
    * Enter a date in future for which you want a prediction for.
    * Select the StationId for which you want to search for.
    * Select the list of pollutants, for which you want to make predictions for.
    * Select the various Environmental Parameters on which you want to see pollutants impact.
    * It is assumed that the last date of any record in the dataset is today's date.
    ### Its an ongoing project ....
    * Currenty the app is working for UP012 region for PM2.5 pollutant.
    """)

    future_date = st.date_input("Date")
    station_id = ('AP001', 'AP005', 'AS001', 'BR005', 'BR006', 'BR008',
                  'BR009', 'BR010', 'CH001', 'DL001', 'DL002', 'DL003', 'DL004',
                  'DL005', 'DL006', 'DL007', 'DL008', 'DL009', 'DL010',
                  'DL012', 'DL014', 'DL015', 'DL016', 'DL017', 'DL018',
                  'DL019', 'DL020', 'DL022', 'DL023', 'DL024', 'DL025',
                  'DL026', 'DL027', 'DL028', 'DL029', 'DL030', 'DL031', 'DL032',
                  'DL034', 'DL035', 'DL036', 'DL037', 'DL038', 'GJ001',
                  'HR011', 'HR012', 'HR013', 'JH001', 'KA002', 'KA003',
                  'KA004',
                  'KA011', 'KL004', 'KL007', 'KL008', 'MH005', 'MH006',
                  'MH007', 'MH008', 'MH009', 'MH010', 'MH011', 'MH012', 'MH013',
                  'MH014', 'ML001', 'MP001', 'MZ001', 'OD001', 'OD002', 'PB001',
                  'RJ004', 'RJ005', 'RJ006', 'TG001', 'TG002', 'TG003', 'TG004',
                  'TG006', 'TN002', 'TN005',
                  'UP012', 'UP013', 'UP014', 'UP015', 'UP016', 'WB007', 'WB008',
                  'WB009', 'WB010', 'WB011', 'WB012', 'WB013')
    options_station = list(range(len(station_id)))
    station_select = st.selectbox("Station ID", options_station, format_func=lambda x: station_id[x])
    pollutant = ("PM2.5", "PM10", "NO", "NO2", "NOx", "NH3", "CO", "SO2", "O3", "Benzene", "Toulene", "Xylene")
    options_pollutant = list(range(len(pollutant)))
    pollutant_select = st.multiselect("Pollutant", options_pollutant, format_func=lambda x: pollutant[x])
    environment = ("Human Health", "Monumental Impact", "Impact on Flora", "Impact on Fauna")
    options_environment = list(range(len(environment)))
    env_select = st.multiselect("Environment", options_environment, format_func=lambda x: environment[x])

    if st.button("Predict"):
        if future_date < date.today():
            st.error("Read the instructions Carefully.")
        else:

            for i in pollutant_select:
                st.write(os.listdir())
                st.write(os.getcwd())
                result = future_predict(station_id[station_select], pollutant[i], future_date)
                st.write("Predicted Value of {} at {} on date {} is : {}".format(pollutant[i],
                                                                                 station_id[station_select],
                                                                                 future_date, result))
            # except:
            # st.error("Record for {} at {} not found.".format(pollutant[i], station_id[station_select]))


if st.button("About"):
    st.text("Developed By Bhavya Goel")
    st.text("Team Fourth Dimension")
    st.text("Future Update will make it realtime")

if __name__ == '__main__':
    main()
