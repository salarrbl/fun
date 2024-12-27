#!/bin/bash

if [ -z "$1" ]; then
  echo "Usage: $0 <playlist-url>"
  exit 1
fi

PLAYLIST_URL=$1

HTML_CONTENT=$(curl -s "$PLAYLIST_URL")

AUDIO_URLS=$(echo "$HTML_CONTENT" | grep -oP 'https?://[^"]+\.(mp3|m4a)')

if [ -z "$AUDIO_URLS" ]; then
  echo "No audio files found on the page. Check the URL or update the regex pattern."
  exit 1
fi

echo "Playing playlist..."
echo "$AUDIO_URLS" | while read -r AUDIO_URL; do
  echo "Playing: $AUDIO_URL"
  mpg123 "$AUDIO_URL"
done

