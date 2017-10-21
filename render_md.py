#!/usr/bin/env python

import codecs
import jinja2
import markdown
import optparse
import re


CURRENT_POST = "Rash Decisions"

ARCHIVED_POSTS = (
    "Backstory",
    "The Plane",
    "The Runway",
)


# Markdown render function with presets.
def md(s):
    md_ext = [
        'markdown.extensions.fenced_code',
        'markdown.extensions.smarty',
    ]
    return markdown.markdown(s, extensions=md_ext)


def read_file(file_path):
    # Read input file in UTF8
    with codecs.open(file_path, encoding='utf-8', mode='r') as fh:
        return fh.read()
        

def write_file(file_path, content_str):
    # Write to file as UTF8.
    with codecs.open(file_path, encoding='utf-8', mode='w') as fh:
        fh.write(content_str)


class Post(object):
    def __init__(self, name):
        self.name = name
        self.id = name.lower().replace(' ', '_')
        self.file_path = 'posts/{}.md'.format(self.id)
        self.body = self.render()

    def render(self):
        html_str = md(read_file(self.file_path))

        # Hack in containers with specified classnames.
        # This takes advantage of the fact that the fenced_code extension
        # will insert the fence language as a classname. But we also want
        # markdown inside the fence, not literal code. So scrape for the
        # classname and the code inside the fence, then re-wrap it and
        # forcibly render it.

        fence_pattern = r'<pre><code class="([a-z -]*?)">(.*?)</code></pre>'
        fence = re.compile(fence_pattern, flags=re.DOTALL)

        def repl(match):
            return r'<div class="{}">{}</div>'.format(
                match.group(1), md(match.group(2)))

        return fence.sub(repl, html_str)


parser = optparse.OptionParser()
parser.add_option("-a", "--all", action="store_true", dest="render_all",
                  default=False, help="render current post and archive")

(options, args) = parser.parse_args()


def main(render_all):

    jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))

    index_template = jinja_env.get_template('index.html')
    html_str = index_template.render(post=Post(CURRENT_POST))
    write_file('static/index.html', html_str)

    if render_all:
        archive_template = jinja_env.get_template('archive.html')
        html_str = archive_template.render(
            archived_posts=[Post(p) for p in ARCHIVED_POSTS])
        write_file('static/archive.html', html_str)


if __name__ == "__main__":
    main(options.render_all)
