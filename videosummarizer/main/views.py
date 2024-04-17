from django.shortcuts import render
from django.http import HttpResponse
from youtube_transcript_api import YouTubeTranscriptApi as yta
from transformers import pipeline
import re

summarizer = pipeline("summarization", model = 't5-base', tokenizer='t5-base', framework='pt')

def index(request):
    if request.method == "POST":
        link = request.POST.get("username")
        ans = process(link)
        context ={'result' :ans}
        return render(request,'result.html',context)
    
    return render(request,'index.html',{})




def extract_video_id(url):
    pattern = r'(?<=v=)[\w-]+'
    match = re.search(pattern, url)
    if match:
        return match.group(0)
    else:
        return None

def process(link):
    url = link
    video_id = extract_video_id(url)
    print(video_id)  # Output: eVX0QrvjA5M

    data = yta.get_transcript(video_id)

    transcript = ''
    for value in data:
        for key, val in value.items():
            if(key == 'text'):
                transcript += val
    l = transcript.splitlines()

    final_text = " ".join(l);

    summary = summarizer(final_text, max_length = 500, min_length = 10, do_sample = False)

    return summary[0]['summary_text'];