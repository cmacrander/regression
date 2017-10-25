#!/bin/bash

./render_md.py --all

gcloud app deploy --project=regression-io --version=production --quiet app.yaml
