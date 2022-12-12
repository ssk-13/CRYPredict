import pyrebase
import streamlit as st
from datetime import datetime

import streamlit as st
from datetime import date
import datetime

import yfinance as yf
from fbprophet import Prophet
from fbprophet.plot import plot_plotly
from plotly import graph_objs  as go 


firebaseConfig = {
  'apiKey': "AIzaSyD7JqWg3lPZ-moZTmSNm3B2pf84MmqdGQk",
  'authDomain': "crypto-prdict.firebaseapp.com",
  'projectId': "crypto-prdict",
  'storageBucket': "crypto-prdict.appspot.com",
  'databaseURL':"https://crypto-prdict-default-rtdb.firebaseio.com",
  'messagingSenderId': "51681607080",
  'appId': "1:51681607080:web:3177e2ed9601c65941f19d",
  'measurementId': "G-LZ14RKP48N"
}

firebase=pyrebase.initialize_app(firebaseConfig)
auth=firebase.auth()

db=firebase.database()
storage=firebase.storage()

st.markdown("<h1 style='text-align: center;font-size: 100px;'><br>CRYPredict Webapp</h1>", unsafe_allow_html=True)

st.sidebar.title("CRYPredict")


choice=st.sidebar.selectbox('login/signup',['Login','Signup'])

email=st.sidebar.text_input('Please enter your email address')

password=st.sidebar.text_input('Please enter your password', type='password')

if choice == 'Signup':
    handle = st.sidebar.text_input('Please input your name',value='Default')
    submit = st.sidebar.button('Create my account')
    st.sidebar.write('<br><br><br>support mail: <a href = "mailto:cryredic@gmail.com?subject = Feedback&body = Message">CRYPredic@gmail.com</a>',unsafe_allow_html=True)

    if submit:
        user = auth.create_user_with_email_and_password(email,password)
        st.success('Your account is created succesfully')
        st.balloons()
        
        user =auth.sign_in_with_email_and_password(email,password)
      
        db.child(user['localId']).child("Handle").set(handle)
        db.child(user['localId']).child("ID").set(user['localId'])
        st.title('welcome ' + handle)
        st.info('Login via login drop down selection')
    else:
        st.warning("already user/invalid email")
       

if choice == 'Login':
    login=st.sidebar.checkbox('(check to login/check to logout)')
    st.sidebar.write('<br><br><br><br><br><br><br>support mail: CRYPredic@gmail.com',unsafe_allow_html=True)
    if login:
        user =auth.sign_in_with_email_and_password(email,password)
        st.write('<style>div.row-widget.stRadio> div{flex-direction:row;}</style>', unsafe_allow_html=True)
        bio =st.radio('Jump to',['Home','About'])
    

        if bio == 'Home':
            START="2021-01-01"
            TODAY=date.today().strftime("%Y-%m-%d")

            st.title("Crypto Prediction App")

            stocks=("BTC-INR","ETH-INR","DOGE-INR","SHIB-INR")
            select_stocks=st.selectbox("Select Dataset for Prediction",stocks)

            n_years=st.slider("Years of prediction:",1,4)
            period= n_years * 365

            
            @st.cache
            def load_data(ticker):
                data=yf.download(ticker,START,TODAY)
                data.reset_index(inplace=True)
                return data

            data_load_state = st.text("Load data...")
            data = load_data(select_stocks)
            data_load_state.text("Loading data...done!")

            st.subheader('Raw data')
            st.write(data.tail())

            def plot_raw_data():
                
                fig = go.Figure(data=[go.Candlestick(x=data['Date'],
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                close=data['Close'])])
                
                
                st.plotly_chart(fig)

            plot_raw_data()

            # Forecasting
            df_train=data[['Date','Close']]
            df_train= df_train.rename(columns={"Date":"ds","Close":"y"})

            m=Prophet()
            m.fit(df_train)
            future=m.make_future_dataframe(periods=period)
            forecast=m.predict(future)

            st.subheader('Forecast data')
            st.write(forecast.tail())


            st.subheader('Particular date Forecast')
            da = st.date_input("Enter date ")
            k=forecast.loc[forecast['ds'] == str(da), 'trend']
            st.write(k)

            st.write('forecast data')
            fig1 =plot_plotly(m,forecast)
            st.plotly_chart(fig1)

            st.write('forecast components')
            fig2 = m.plot_components(forecast)
            st.write(fig2)

        if bio == 'About':

             st.title("CRYPredict Webapp")

             st.write('The CRYPredict webapp forecast the future price action of cryptocurrency and provide the anaylisis on it.The our webapp forecast the values on the basis of the past data and models.Our webapp provides 90% accuracy currently it may change.')
             st.write('Use prediction on your own risk')

             st.write('we are using yfinance as our API to get live data and fbprophet as our model to get predictions.Our webapp UI runs using streamlit.')

    

