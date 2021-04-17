# isalive
Takes a list of urls and check if they still lead to the same page

## Usage 
### Flags
```
  -u URLS       File containing target urls
  -o OUTPUT     Output file for urls with status 200
  -f FORBIDDEN  Output file for urls with status 403
  -t THREADS    Threads
```

### Examples
```
$ python3 isalive.py -u wayback.urls -o nice.ones -t 32
```
