from flask import Flask, request, render_template
import yfinance as yf
from twilio.rest import Client
import smtplib ,ssl
import schedule, time
import os

app = Flask(__name__)

@app.route('/') 
def index():
    return render_template('index.html')
@app.route('/',methods = ['POST'])
def process():
    #if request.method == 'POST':
    stock_ticker = request.form['stock_ticker']
    threshold = float(request.form['threshold'])
    frequency = request.form['frequency']
    notification_medium = request.form['notification_medium']
    user_phone_number = request.form['phone']
    user_email = request.form['email']
    #return render_template('info.html',stock_ticker=stock_ticker,threshold=threshold)
    # Convert frequency to seconds
    while True:
        # Fetch current stock price
        stock_data = yf.Ticker(stock_ticker).info
        current_price = stock_data['currentPrice']
        #print(current_price)
        # Check if current price crosses the threshold
        if current_price >= threshold:
            # Send notification to user via Twilio API or Email
            if notification_medium == 'text':
                account_sid = os.environ['your twilio id']
                auth_token = os.environ['your twilio token']
                client = Client(account_sid, auth_token)

                message = client.messages.create(
                                    body=f" Dear User,Curretn price of your stock {stock_ticker}  is {current_price}.You have set threshold at {threshold}.",
                                    from_='your twilio phone number',
                                    to= str(+977)+user_phone_number
                                )

                print(message.sid)
                break
            elif notification_medium == 'email':
                your_mail=' type Your email here'
                your_mail_pw =' your 16 digits pw generated from google for third party  authentication in 2f authentication'
                server = smtplib.SMTP('smtp.gmail.com', 587)
                context = ssl.create_default_context()
                server.starttls(context=context)
                server.login(your_mail,your_mail_pw )

                message = f"Subject: Stock Price Notification\n\nStock price of {stock_ticker} has reached price: {current_price}.You have set threshold at {threshold}."
                server.sendmail(your_mail, user_email, message)
                server.quit()
                break
            else:
                return "Invalid notification medium"

    return render_template('info.html',stock_ticker= stock_ticker, current_price= current_price, threshold = threshold)
# for scheduling notification
def schedule_notification():
    schedule.every().minute.do(process)
    schedule.every(1).hour.do(process)
    schedule.every().day.at("3:00").do(process)
    schedule.every().monday.do(process)
    while True:
        schedule.run_pending()
        time.sleep(1)
if __name__ == '__main__':
    app.run(debug=True)
