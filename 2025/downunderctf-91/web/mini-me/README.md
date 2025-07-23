# Solution

the source code hints us that we need the `API-Key` secret, but there nothing vulnerable with source code we get except _js_ file, let's look at it.

there are some comment in the end shows that there's a _test-main_ js file.

after request for that file, we can get the `API-Key` leak.

```bash
curl -X POST 'https://web-mini-me-ab6d19a7ea6e.2025.ductf.net/admin/flag' -H 'X-API-Key: TUNG-TUNG-TUNG-TUNG-SAHUR'
```
