#!/usr/bin/env bash
command -v brew >/dev/null || (echo 'Please install homebrew first (opening home page for you now…' && sleep 1 && open 'http://brew.sh' && exit)
brew install fish chromedriver
echo 'Need an admin password to install Selenium browser automation framework'
sudo pip install selenium
