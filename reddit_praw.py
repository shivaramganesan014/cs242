import re
import praw
from praw.models import MoreComments


def get_string(text):
	return re.sub('[^a-zA-Z0-9 \n\.]', '', text)


reddit = praw.Reddit(

	client_id="123",

	client_secret="123",

	user_agent="123" )

# print(reddit.read_only) # Output: True

delimitter = "\n"
emptystring_placeholder = "${EMPTY}"


limit = 5

redditlist = [
	"howto",
	"askreddit",
	"trueaskreddit",
	"askacademia",
	"askcomputerscience",
	"askstatistics",
	"askscitech",
	"explainlikeimfive",
	"answers",
	"whatisthisthing",
	"nostupidquestions",
	"help"
]


for subreddit in redditlist:
	print("getting data from r/"+subreddit)

	output_file_name = subreddit+".jsonl"
	open(output_file_name, "w").close()

	output_file = open(output_file_name, "a")
	output_file.write("[")

	index = 0

	for submission in reddit.subreddit(subreddit).hot(limit=limit):
		json = {}
		json['title'] = get_string(submission.title)
		json["score"] = submission.score
		json["id"] = submission.id
		json["url"] = submission.url
		json["body"] = get_string(submission.selftext)
		if(json["body"] == ""):
			json["body"] = emptystring_placeholder
		comments = []
		for comment in submission.comments.list():
			if isinstance(comment, MoreComments):
				continue
			comment_json = {}
			comment_json["body"] = get_string(comment.body)
			comment_json["score"] = comment.score
			comments.append(comment_json)
		json['comments'] = comments
		
		outstring = str(json)
		if(index < limit-1):
			outstring+=','
		output_file.write(outstring)
		output_file.write(delimitter)
		index+=1

output_file.write("]")

output_file.close()
	