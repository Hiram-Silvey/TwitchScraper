import requests, time
import cfg

URL_PREFIX = 'https://api.twitch.tv/v5/videos/'

def build_url(vid, offset=None, cursor=None):
    url = URL_PREFIX + '{}/comments?client_id={}'.format(vid, cfg.CLIENT_ID)
    if cursor is not None:
        url += '&cursor={}'.format(cursor)
    elif offset is not None:
        url += '&content_offset_seconds={}'.format(offset)
    return url

def get_chunk(url):
    for retries in range(3, -1, -1):
        chunk_req = requests.get(url)
        if not chunk_req.ok:
            print('ERR: unable to fetch URL {}'.format(url), end='')
            if retries > 0:
                print(', {} tries remaining...'.format(retries))
                time.sleep(1)
                continue
            else:
                print()
                return None
        break
    return chunk_req.json()

def get_closest_chunk(vid, offset):
    url = build_url(vid, offset=offset)
    while True:
        chunk = get_chunk(url)
        if chunk is None:
            return None
        if chunk['comments'][0]['content_offset_seconds'] <= offset:
            break
        cursor = chunk['_prev']
        url = build_url(vid, cursor=cursor)
    return chunk

def get_next_chunk(chunk):
    vid = chunk['comments'][0]['content_id']
    cursor = chunk.get('_next')
    if cursor is None:
        return None
    url = build_url(vid, cursor=cursor)
    return get_chunk(url)

def get_chat(vid, offset_start, offset_end):
    chat = []
    curr_offset_start = offset_start
    curr_chunk = get_closest_chunk(vid, offset_start)
    while True:
        if curr_chunk is None:
            break
        comments = curr_chunk['comments']
        for comment in comments:
            curr_offset = comment['content_offset_seconds']
            if curr_offset > offset_end:
                break
            if curr_offset <= curr_offset_start:
                continue
            commenter = comment['commenter']['_id']
            message = comment['message']['body']
            chat.append((commenter, str(curr_offset-offset_start), message))
        curr_offset_start = curr_offset
        curr_chunk = get_next_chunk(curr_chunk)
    return chat
