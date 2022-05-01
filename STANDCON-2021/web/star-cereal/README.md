# Star Cereal

**Author**: zeyu2001

**Category**: Web

[Solution](solve/solve.md)

## Problem Statement

Have you heard of Star Cereal? It's a new brand of cereal that's been rapidly gaining popularity amongst astronauts - so much so that their devs had to scramble to piece together a website for their business! The stress must have really gotten to them though, because a junior dev accidentally leaked part of the source code...

## Summary

A PHP object injection vulnerability exists in the login process. When the user attempts to log in, the POST data is used to create a Login object, which is then serialized and set as the login cookie for subsequent authentication.

Using the `process_login.php` source code, participants are required to craft an exploit that bypasses all verification checks through a POP chain. Once an appropriate login cookie is crafted, participants can log in successfully and obtain the flag.

## Deployment

`docker-compose up -d`

The vulnerable web application will then be accessible through port 8100.

## Distributed Files

- `process_login.php`
