import re
import praw
from praw.models import MoreComments
# from praw.handlers import MultiProcessHandler
import time
import json
# from time import sleep


def write_to_file(file_name, contents):
	with open(file_name, "r+") as file:
		file_data = json.load(file)
		for content in contents:
			file_data.append(content)
			file.seek(0)
		json.dump(file_data, file)


def get_string(text):
	return re.sub('[^a-zA-Z0-9 \n\.]', '', text)


# handler = MultiProcessHandler()
reddit = praw.Reddit(
	client_id="",
	client_secret="",
	user_agent=""
	# handler = handler
)

# print(reddit.read_only) # Output: True

delimitter = "\n"
emptystring_placeholder = "${EMPTY}"

output_dir = "data/"
limit = 1000

redditlist = [
	"howto",
	"askreddit",
	"trueaskreddit",
	"askacademia",
	"askcomputerscience",
	"askstatistics"
	"askscitech",
	"explainlikeimfive",
	"answers",
	"whatisthisthing",
	"nostupidquestions",
	"help"
	"youshouldknow",
	"sciencesubreddits",
	"askscience",
	"mathematics",
	"engineering",
	"technology",
	"tech",
	"techsupport",
	"learnprogramming"
	#-------------
	# "tooafraidtoask",
	# "morbidquestions",
	# "AMA",
	# "webdev",
	# "web_design",
	# "buildapc",
	# "worldnews",
	# "news",
	# "worldevents",
	# "business",
	# "economics",
	# "education",
	# "history",
	# "politics2",
	# "politics",
	# "uspolitics",
	# "americanpolitics",
	# "progressive",
	# "socialism",
	# "libertarian",
	# "anarchism",
	# "democrats",
	# "liberal",
	# "republican",
	# "liberty",
	# "democracy"



]

write_threshold = 100;

start_time = time.time();

for subreddit in redditlist:

	begin = time.time()
	print("getting data from r/"+subreddit)

	output_file_name = output_dir+subreddit+".jsonl"
	# open(output_file_name, "w").close()

	output_file = open(output_file_name, "a")
	# output_file.write("[")
	output_text = []
	output_file.write(json.dumps(output_text))
	output_file.close()

	# index = 0

	length = 0


	for submission in reddit.subreddit(subreddit).hot(limit=None):
		json_dict = {}
		json_dict["title"] = get_string(submission.title)
		json_dict["score"] = submission.score
		json_dict["id"] = submission.id
		json_dict["url"] = submission.url
		json_dict["body"] = get_string(submission.selftext)

		if(json_dict["body"] == ""):
			json_dict["body"] = emptystring_placeholder

		comments = []
		for comment in submission.comments.list():
			if isinstance(comment, MoreComments):
				continue
			comment_json = {}
			comment_json["body"] = get_string(comment.body)
			comment_json["score"] = comment.score
			comments.append(comment_json)
		json_dict["comments"] = comments
		
		output_text.append(json_dict)
		length += 1

		if(length >= write_threshold):
			write_to_file(output_file_name, output_text)
			output_text = []
		

		# outstring = str(json_dict)
		# if(index < limit-1):
		# 	outstring+=','
		# output_file.write(outstring)
		# output_file.write(delimitter)
		# index+=1
		time.sleep(2)

	if(len(output_text) > 0):
		write_to_file(output_file_name, output_text)
		output_text = []

	end = time.time()

	print(f"completed in {end-begin}")
	# output_file.write("]")
end_time = time.time();
print(f"scraping done in  {end_time-start_time}")
# output_file.close()
	