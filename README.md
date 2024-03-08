# Retrieve Relevant HackerNews Stories
This retrieves the top 500 HackerNews stories, ordered based on relevance to the given bio.

The program retrieves the top 500 HN stories. It then isolates the nouns, proper nouns, and plural nouns from the bio, the story titles, and story body (if it exists). Matches between the bio and the stories are then identified. Matches with the title of a story counts for two, since a title word is more representative of the story than a body word. This score is then used to sort the list of 500 stories, and then displayed.

The thought process is that these key words pulled from the bio and posts can identify what the bio or post is about, and therefore we can then determine relevance from that.

This was optimized for dev time, so of course this is far from the optimal solution. It is also quite slow.

[Live Demo](https://0or42p1b4e.execute-api.ca-central-1.amazonaws.com/dev)
[API](https://0or42p1b4e.execute-api.ca-central-1.amazonaws.com/dev/api)
