# FinalCode-Twitter

Running the server:


●	Go to Linode server: https://cloud.linode.com/linodes Reboot the server.


●	Open terminal. Enter command
ssh sats@45.79.181.198

When it asks for password enter this password: confluence909090

●	To start our server we need to enter the virtual environment. For that use command:
source venv/bin/activate

●	Type cd buttonpython/ to enter buttonpython directory

●	Start server using:
gunicorn --bind 0.0.0.0:8000 buttonpython.wsgi -t 1200

●	Go to AWS page. Check if serve is running. Check if dashboard is working on:   

●	Start a new terminal window. Type following commands:

○	ssh sats@45.79.181.198
When it asks for password: confluence909090
○	cd buttonpython/
○	./script.sh

This starts our servers -both linode and AWS and the script which transfers the csv data to dashboard.

Code Explaination:
●	The code is present is DataExtraction.py. The first part of the code deals with connecting to Twitter API. The twitter credentials are present in credentials.csv. We extract the tweet URLs by scraping the tweets with our conditions

●	The second part consists of extracting the actual tweet from the tweet URLs. The extract_tweets() function describes the fields we are extracting. The data is extracted in batches to avoid timeout.

●	The third part consists of Sentiment Analysis. Here we do the following steps:
○	Converting to lowercase
○	Removing punctuation
○	Removing stopwords
○	Lemmatization
○	Calculating Polarity scores

