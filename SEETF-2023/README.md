# SEETF 2023

Here are the challenges I made for SEETF 2023, the inaugural CTF held by [Social Engineering Experts](https://ctftime.org/team/151372).

| Challenge                                           | Summary                                                                              | Category | Solves |
|-----------------------------------------------------|--------------------------------------------------------------------------------------|----------|--------|
| [ezXXE](./ezxxe/)                                                | A bunch of XXE regex bypasses                                                        | Web      | 4      |
| [Now You C Me](./now-you-c-me/)                                  | Custom HTTP server vulnerable to integer overflow, leading to client-side desync     | Web      | 4      |
| [readonly](./readonly/)                                          | Command injection in PEARcmd without needing a writeable filesystem                  | Web      | 4      |
| [Mandatory Notes Challenge](./mandatory-notes-challenge/)        | Navigation XS-Leak challenge using Chrome's max URL length and long URL fragments    | Web      | 5      |
| [Wasmabism](./wasmabism/)                                        | WASM exploitation: buffer overflow to overwriting function pointers and XSS          | Web      | 5      |
| [Star Cereal Episode 4: A New Pigeon](./star-cereal/)            | 0day in serialize-javascript library + CSP bypass through www.youtube.com JSONP      | Web      | 7      |
| [PlantUML](./plantuml/)                                          | 0day URL whitelist bypass to SSRF and local file read in latest version of PlantUML  | Web      | 11     |
| [Sourceful Guessless Web](./sourceful-guessless-web/)            | Making use of ini_set PHP directives to control assert callback and read local files | Web      | 12     |
| [Express JavaScript Security](./express-javascript-security/)    | RCE through unrestricted options on latest version of EJS                            | Web      | 45     |
| [Shellcode As A Service](./SaaS/)                                | 6 bytes of shellcode, only open and read syscalls allowed                            | Pwn      | 41     |
