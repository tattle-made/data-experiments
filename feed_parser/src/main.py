import feedparser
import dateutil.parser

urls = []

feeds = [feedparser.parse(url) for url in urls]

for index, _ in enumerate(feeds):
    print(feeds[index].keys())
    if feeds[index].bozo:
        # if feeds are not well-formed - bozo detection
        # https://feedparser.readthedocs.io/en/latest/bozo.html
        exc = feeds[index].bozo_exception
        print(exc, ' message:', exc.getMessage(), ' line:', exc.getLineNumber())
        raise ValueError

# get publication_name
publication_name = []
missing_title = 'missing publication name'
for feed in feeds:
    if 'title' in feed['feed']:
        publication_name.append(feed['feed']['title'])
    else:
        # TODO: verify if raise error instead here
        publication_name.append(missing_title)

for index, url in enumerate(urls):
    # get item entries
    if feeds[index].keys() >= {'entries'}:
        feed_entries = feeds[index]['entries']
        print(feed_entries[0].keys())
        required_fields = {'title', 'author', 'published', 'link'}
        if not feed_entries[0].keys() >= required_fields:
            # all keys in required_fields should be present
            raise ValueError

        # get all feeds in reverse chronological order
        feed = [item for item in feed_entries]
        feed.sort(key=lambda x: dateutil.parser.parse(x['published']), reverse=True)
        publication = publication_name[index]
        for idx in feed:
            print({'publication:': publication, 'title': idx['title'], 'author': idx['author'], 'date': idx['published'],
                   'link': idx['link']})
    else:
        raise ValueError
