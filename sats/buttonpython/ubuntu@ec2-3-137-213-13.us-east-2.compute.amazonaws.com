input {
    file {
        path => "/home/sats/buttonpython/postweets.csv"
        start_position => "beginning"
        }
 }

 filter {
        csv{
            separator => ","
            columns => ["Sno","tweet_ID","username","lemmatize","polarity"]
        } 
}	

 output{
        elasticsearch{
            hosts => "http://3.133.139.66:9200"
            index => "index_i_pt3"
	    document_id => "%{tweet_ID}"
	}

        stdout {}
 }
