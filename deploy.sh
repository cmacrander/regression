#!/bin/bash

./render_md.py --all

gcloud app deploy --version=production --quiet app.yaml
