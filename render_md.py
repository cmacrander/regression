#!/usr/bin/env python

import codecs
import markdown
import re
import sys

# Get input file from command line
input_filename = sys.argv[1]

# Output file of same name but file extension .html
output_filename = input_filename.split('.')[0] + '.html'

# Read input file in UTF8
with codecs.open(input_filename, encoding='utf-8', mode='r') as fh:
    md_str = fh.read()

# Markdown render function with presets.
def md(s):
    md_ext = [
        'markdown.extensions.fenced_code',
        'markdown.extensions.smarty',
    ]
    return markdown.markdown(s, extensions=md_ext)

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

html_str = code_fence.sub(repl, html_str)

# Write to file as UTF8.
with codecs.open(output_filename, encoding='utf-8', mode='w') as fh:
    fh.write(html_str)
