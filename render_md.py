#!/usr/bin/env python

import codecs
import jinja2
import markdown
import optparse
import re

CURRENT_POST = 'RDU'

ARCHIVED_POSTS = (
    'Backstory',
)

parser = optparse.OptionParser()
parser.add_option("-a", "--all", action="store_true", dest="render_all",
                  default=False, help="render current post and archive")

(options, args) = parser.parse_args()

# Markdown render function with presets.
def md(s):
    md_ext = [
        'markdown.extensions.fenced_code',
        'markdown.extensions.smarty',
    ]
    return markdown.markdown(s, extensions=md_ext)

def render_post(post_name):
    input_filename = 'posts/{}.md'.format(post_name)

    # Read input file in UTF8
    with codecs.open(input_filename, encoding='utf-8', mode='r') as fh:
        md_str = fh.read()

    # Render.
    html_str = md(md_str)

    # Hack in containers with specified classnames.
    # This takes advantage of the fact that the fenced_code extension
    # will insert the fence language as a classname. But we also want
    # markdown inside the fence, not literal code. So scrape for the
    # classname and the code inside the fence, then re-wrap it and
    # forcibly render it.

    code_fence_pattern = r'<pre><code class="([a-z -]*?)">(.*?)</code></pre>'
    code_fence = re.compile(code_fence_pattern, flags=re.DOTALL)

    def repl(match):
        return r'<div class="{}">{}</div>'.format(
            match.group(1), md(match.group(2)))

    return code_fence.sub(repl, html_str)

def write_file(filepath, content_str):
    # Write to file as UTF8.
    with codecs.open(filepath, encoding='utf-8', mode='w') as fh:
        fh.write(content_str)

def main(render_all):

    jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))

    index_template = jinja_env.get_template('index.html')
    html_str = index_template.render(current_post=render_post(CURRENT_POST))
    write_file('static/index.html', html_str)

    if render_all:
        archive_template = jinja_env.get_template('archive.html')
        archived_posts = [render_post(p) for p in ARCHIVED_POSTS]
        html_str = archive_template.render(archived_posts=archived_posts)
        write_file('static/archive.html', html_str)


if __name__ == "__main__":
    main(options.render_all)

