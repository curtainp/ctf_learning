### FlagGuessr (+ Revenge)
Due to the way `Register()` works with sessions, triggering the last `bad request` will cause the JWT payload you send in the request to be signed in the response, other explanations in the Discord go through this more thoroughly. This was possible to trigger if the `INSERT` fails even though the `CheckUsernameAvailable()` thinks the username should be available. It can fail because of `PRIMARY KEY (username, display_name)` if both the username and display name already exist. We did this using a race condition because they both pass the check at first, but one gets inserted before the other and errors, causing our arbitrary JWT to be signed. (shoutout <@407861521645830144>)

From there, you could inject arbitrary environment variables in `session.Properties` which is triggered via `MakeCert`. It calls a shell command, so having arbitrary environment variables in here is dangerous. `LD_PRELOAD` works because it calls `cp` itself which is a dynamically linked executable, loading the path we set in the value first. We can write the payload by uploading it as our "flag.txt", then referencing it like:
```json
"properties": {
  "LD_PRELOAD": "/app/userdata/d78ef477-f9e7-403b-8980-1d4731b8eec7/flag.txt"
},
```
For the revenge a race condition isn't possible anymore due to locks and a lot more steps are required to trigger the `bad request` error. The important bit is that `CheckUsernameAvailable()` compares usernames in Go, case-sensitively. While the `username` column in SQLite is defined with `COLLATE NOCASE` meaning casing doesn't matter. While it may now sound trivial do just register two users with different casing to trigger the error, `Username: strings.ToLower(username)` makes this impossible.
