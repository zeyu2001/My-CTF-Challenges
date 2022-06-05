# Super Secure Requests Forwarder - Solution

**Author**: zeyu2001

**Category**: Web

The validation mechanism is flawed - the URL is fetched once to check whether an SSRF is attempted, and then fetched a second time once it is determined to be legitimate.

We can run a server that gives two different responses, passing the check the first time and redirecting to `http://localhost/flag` the second time.