## Functions to analyze a post being created by a user

import json

from actions.analysis.common import compute_similarity

# Get posts similar to user's input
def similar_posts(handle, similarity_model, post_text):
    similar_cur = handle.cursor(dictionary = True)
    similar_cur.execute('select * from posts')
    post_res = similar_cur.fetchall()
    #Compute similarity scores
    scores = dict()
    for post in post_res:
        id = post['post_id']
        content = post['content']
        sim_score = compute_similarity(similarity_model, post_text, content)
        if sim_score < 0:
            continue
        scores[id] = [content, sim_score]
    #Return as JSON
    return json.dumps(scores)