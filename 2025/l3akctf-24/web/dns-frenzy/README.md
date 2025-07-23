# Description

1.1.1.1? 8.8.8.8? Nah, I built my own custom DNS resolver with internal subdomains!

Port Mappings: 17004 -> 5335 and 17014 -> 53535

Author: p.\_.k

[](http://34.134.162.213:17004)

# Solution

The `flag` will leak with following condition match:

1. the query domain name contains `dns_l3ak.ctf`
2. the query domain resolves to `127.0.0.1`

## Wildcard DNS

the [nip](nip.io) which is a wildcard dns service that maps `x.x.x.x.nip.io` to `x.x.x.x`, so:

```bash
  127.0.0.1.dns_l3ak.ctf.nip.io => 127.0.0.1
```

## Conclusion

- DNS TXT records can be used to embed hidden data
- IP-based logic and domain patterns can be tricks using services like `nip.io`
