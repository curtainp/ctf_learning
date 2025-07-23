# Solution

the main issue with the web application is that user's `currency` is fetched from the session cookie when converting their balance and checking if they are rich.

the application don't validate the session' currency. so we can reuse the old session to quickly increase the balance.

```bash
  # 1. first we register and login to get a normal user with 50 AUD balance.
  # 2. then we convert this currency to   GBP, which is the most expensive, and we save this session which server set for reuse.
  # 3. then we reuse above session to convert currency to IDR, which is the cheapest, make balance blowing up quickly.
```
