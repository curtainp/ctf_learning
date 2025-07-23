nc chal.2025.ductf.net 30015

# Solution

when we use `nc` to connect to the server, any input we send just return 2.

and the description hints us that _horoscope_ and the little Tommy is a _Taurus_ and a month before matching his mum and dad, so his mum and dad is _Gemini_ horoscope.

the `openssl` has a cli option to perform a gemini client:

```bash
openssl s_client -connect chal.2025.ductf.net:30015 -crlf -ign_eof

# after receive some header info, we request gemini with that url
gemini://chal.2025.ductf.net
```

or we also access that information with a normal client. some like [lagrange](https://git.skyjake.fi/gemini/lagrange)
