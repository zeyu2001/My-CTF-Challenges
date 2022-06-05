# Welcome

**Author**: zeyu2001

**Category**: Misc

## Description

< Insert YouTube video and download link here >

Welcome to SEETF! Submit the teaser video flag here.

## Difficulty

Medium

## Solution

Towards the end of the video, each frame contains one pixel of a QR code (at the top right corner).

The solution is to simply split up the frames and analyze each frame to reconstruct the QR code.

First run `ffmpeg -i trimmed.mp4 -vf fps=60 solve/%d.png`.

Then run the `solve.py` script.
