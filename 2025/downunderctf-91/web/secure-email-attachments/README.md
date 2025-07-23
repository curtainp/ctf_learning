# Solution

the main issue is the use of `filepath.Clean()` to sanitise the user provide path.

> NOTE: the filepath.Clean and path.Clean have a misleading filename and do not clean paths that do not start with `/`, so we can leverage this to directory traversal with `../../`

Second, we need to bypass the validation that checking ensuring that no `..` squences exists in the provided path.

```
  GET /attachments./attachments././attachments./attachments/etc/flag.txt HTTP/1.1
```
