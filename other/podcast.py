import pyaudio,requests,time,thread,subprocess,urllib2,json


def download_file(url):
    local_filename = "podcast.mp3"
    ##local_filename = url.split('/')[-1]
    # NOTE the stream=True parameter
    r = requests.get(url, stream=True)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024): 
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
                #f.flush() commented by recommendation from J.F.Sebastian
    return local_filename

 
def start(stream):    
    thread.start_new_thread ( download_file, (stream,) )
    time.sleep(10)
    subprocess.call(["xdg-open", "podcast.mp3"])
    while True:
        r = raw_input("i play sounds!")
        if r:
            break

global details;details = [] 

   
def getUrl(podcast_id):
        base="https://feedwrangler.net/api/v2/podcasts/show"
        addressurl = base + "?podcast_id="+podcast_id
        req = urllib2.Request(addressurl)
        html = urllib2.urlopen(req).read().decode("utf-8")
        data = json.loads(html)
        if data["result"]=="success":
            for i in data["podcast"]["recent_episodes"][:1]:
                details.append(str(i["audio_url"]))
