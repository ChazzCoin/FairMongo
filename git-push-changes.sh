#!/bin/zsh

sudo rm -rf dist
sudo rm -rf build
sudo rm -rf FairMongo.egg-info

git add .
git commit -m "automated changes"
git push origin main