from bottle import route, run, view, request, static_file, error, HTTPError, get, template
from urllib.parse import urlunsplit
import anipy_cli

def join(p1, p2):
    if p1[len(p1)-1] == "/" and p2[0] == "/":
        return p1[0:len(p1)-1] + p2
    if p1[len(p1)-1] != "/" and p2[0] != "/":
        return p1 + "/" + p2
    return p1 + p2

def make_category_url(show_path):
    return urlunsplit(("https", "gogoanime.gg", show_path, "", ""))

def watch_url(show_path, ep):
    return join(join("/watch/", show_path), str(ep))

def show_path_to_name(show_path):
    segments = show_path.split("/")
    try:
        segments.remove('')
    except:
        pass
    try:
        segments.remove('category')
    except:
        pass
    return segments[0].replace("-", " ")

@error(404)
def error404(error):
    return 'not found.'

@get('/')
def index():
    return static_file("search.html", root='./static')

@get('/static/<filepath:path>')
def static(filepath):
    return static_file(filepath, root='./static')

@get('/show')
@view('base')
def query_show():
    query = request.query.get('query')
    if query is None:
        return 'no query provided.'

    query_class = anipy_cli.query(query, anipy_cli.Entry())
    links = query_class.get_links()
    if type(links) != tuple:
        return 'no results.'

    body = '<ul>\n'
    for i in range(len(links[0])):
        link = links[0][i]
        name = links[1][i]
        body += template(
            '<li><a href="{{href}}">{{name}}</a></li>\n',
            href=join('/show', link), name=name
        )
    body += '</ul>'

    return { 'body': body, 'title': f'search "{query}"' }

@get('/show/<show_path:path>')
@view('base')
def get_episodes(show_path):
    entry = anipy_cli.Entry(category_url=make_category_url(show_path), ep=0)

    ep_class = anipy_cli.epHandler(entry)
    latest_ep = ep_class.get_latest()
    entry = ep_class.get_entry()

    body = '<ul>\n'
    for i in range(latest_ep):
        ep = i+1
        body += template(
            '<li><a href="{{href}}">episode {{ep}}</a></li>\n',
            href=watch_url(show_path, ep), ep=ep
        )
    body += '</ul>'

    return { 'body': body, 'title': show_path_to_name(show_path) }

@get('/watch/<show_path:path>/<ep>')
@view('player')
def watch(show_path, ep):
    ep = int(ep)
    entry = anipy_cli.Entry(
        category_url=make_category_url(show_path),
        ep=ep,
    )

    ep_class = anipy_cli.epHandler(entry)
    latest_ep = ep_class.get_latest()
    entry = ep_class.gen_eplink()

    url_class = anipy_cli.videourl(entry, "best")
    url_class.stream_url()
    entry = url_class.get_entry()

    body = f"<h3 style='margin-top: 0; margin-bottom: 0.5rem'>episode {ep}</h3>"
    body += "<div style='margin-bottom: 0.75rem'>"
    if ep > 0:
        body += template(
            '<a href="{{href}}">previous episode</a>\n',
            href=watch_url(show_path, ep-1),
        )
    body += template(
        '<a href="{{href}}">episode list</a>\n',
        href=join('/show', show_path)
    )
    if ep < latest_ep:
        body += template(
            '<a href="{{href}}">next episode</a>\n',
            href=watch_url(show_path, ep+1),
        )
    body += "</div>"

    return {
        'video_url': entry.stream_url,
        'body': body,
        'title': f'{ep} | {show_path_to_name(show_path)}'
    }

run(host='0.0.0.0', port=8080)

