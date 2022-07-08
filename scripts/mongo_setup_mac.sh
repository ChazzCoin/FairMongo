#!/bin/zsh

## -> install mongodb via homebrew
brew tap mongodb/brew
brew install mongodb-community@5.0
## -> start mondodb
brew services start mongodb-community