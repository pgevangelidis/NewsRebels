from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from numpy import argsort
import json


def return_indexs_of_the_most_relevant_articles( json_with_articles , query , thres=0.1 , num_of_rel_articles = 15):
    documents = []
    for i in range(0 , len(json_with_articles['articles'])):
        documents.append(json_with_articles['articles'][i]['title'] + json_with_articles['articles'][i]['description'] )
    #print( len(documents))
    #print(len(documents))
    #print("kati")
    tf = TfidfVectorizer(analyzer='word', ngram_range=(1,2), min_df = 0, stop_words = 'english')
    tf_idf_vector_space_articles = tf.fit_transform(documents)
    #print(tf_idf_vector_space_articles.shape)
    tf_idf_query_vector = tf.transform([query])
    #print (tf_idf_vector_space_articles.shape)
    #print(tf_idf_query_vector.shape)
    #print(len(documents))
    #print(cosine_similarity(tf_idf_query_vector, tf_idf_vector_space_articles)[0])
    #print ( argsort(cosine_similarity(tf_idf_query_vector, tf_idf_vector_space_articles)[0] )[::-1][:10] )
    idx = argsort(cosine_similarity(tf_idf_query_vector, tf_idf_vector_space_articles)[0] )[::-1][:num_of_rel_articles]
    sim_val = cosine_similarity(tf_idf_query_vector, tf_idf_vector_space_articles)[0][idx]
    #print (idx)
    #print(sim_val)
    #print (  [ idx[i] for i in range(0 , len(idx )) if sim_val[i] > thres ] )

    ret_json = {}
    relev_doc = []

    for i in  [ idx[i] for i in range(0 , len(idx )) if sim_val[i] > thres ]:
        #print( json_with_articles['articles'][i]["description"] )
        relev_doc.append(json_with_articles['articles'][i])

    ret_json["articles"] = relev_doc

    return ret_json

if __name__ == "__main__":
    print("ksekinaei to IR")


    json_articles = { "articles": [{
					"image": "https://scontent.flcy1-1.fna.fbcdn.net/v/t1.0-9/11113869_10206206558034509_1969151949810844066_n.jpg?_nc_cat=0&_nc_eui2=v1%3AAeFCQdHKjTsfsryAe8FM38BCwlxP5s00zLcJrFwqzopO8QfGi6d7GB3XHl9-T44cMHYHq5IxfP9_ipZM9X3Nf415j-YPTA_5uVg0y1ZBsOSpcQ&oh=bde0889b65c1dbb4677efe651d937ea7&oe=5B348ABD",
					"title": "Clara Ponsati's lawyer says she will hand herself in to police",
					"description": "Clara Ponsati's lawyer tells the BBC she will attend an Edinburgh police station within days.",
					"source": "https://www.hackster.io/groundcontrol/majortom-alexa-voice-controlled-ardrone-2-0-beedb2",
					"date": "02/15/2014"
				  },
				  {
					"image": "https://scontent.flcy1-1.fna.fbcdn.net/v/t1.0-9/11113869_10206206558034509_1969151949810844066_n.jpg?_nc_cat=0&_nc_eui2=v1%3AAeFCQdHKjTsfsryAe8FM38BCwlxP5s00zLcJrFwqzopO8QfGi6d7GB3XHl9-T44cMHYHq5IxfP9_ipZM9X3Nf415j-YPTA_5uVg0y1ZBsOSpcQ&oh=bde0889b65c1dbb4677efe651d937ea7&oe=5B348ABD",
					"title": "Man dies in hospital after Post Office 'disturbance' in Glasgow",
					"description":"Two men have been arrested in connection with the incident in Cardonald, Glasgow, on Saturday afternoon.",
					"source": "https://www.hackster.io/groundcontrol/majortom-alexa-voice-controlled-ardrone-2-0-beedb2",
					"date": "02/15/2014"
				  },
				  {
					"image": "https://scontent.flcy1-1.fna.fbcdn.net/v/t1.0-9/11113869_10206206558034509_1969151949810844066_n.jpg?_nc_cat=0&_nc_eui2=v1%3AAeFCQdHKjTsfsryAe8FM38BCwlxP5s00zLcJrFwqzopO8QfGi6d7GB3XHl9-T44cMHYHq5IxfP9_ipZM9X3Nf415j-YPTA_5uVg0y1ZBsOSpcQ&oh=bde0889b65c1dbb4677efe651d937ea7&oe=5B348ABD",
					"title": "Future fuel quest takes a step forward",
					"description": "Scientists at Heriot Watt University develop a technique that could help make hydrogen fuel a reality",
					"source": "https://www.hackster.io/groundcontrol/majortom-alexa-voice-controlled-ardrone-2-0-beedb2",
					"date": "02/15/2014"
				  },
                  {
					"image": "https://scontent.flcy1-1.fna.fbcdn.net/v/t1.0-9/11113869_10206206558034509_1969151949810844066_n.jpg?_nc_cat=0&_nc_eui2=v1%3AAeFCQdHKjTsfsryAe8FM38BCwlxP5s00zLcJrFwqzopO8QfGi6d7GB3XHl9-T44cMHYHq5IxfP9_ipZM9X3Nf415j-YPTA_5uVg0y1ZBsOSpcQ&oh=bde0889b65c1dbb4677efe651d937ea7&oe=5B348ABD",
					"title": "Heathrow rules out compensation for delayed disabled passengers",
					"description": "The BBC's Frank Gardner had criticised the airport for a delay because his wheelchair was misplaced.",
					"source": "https://www.hackster.io/groundcontrol/majortom-alexa-voice-controlled-ardrone-2-0-beedb2",
					"date": "02/15/2014"
				  }
		  ]
		}


    query = "Clara Ponsati's lawyer tells"
    print( json.dumps(  return_indexs_of_the_most_relevant_articles(json_articles , query) ) )
