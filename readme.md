# Post-update Website Testing

After upgrading a Drupal module, I often find myself wanting to check that several pages (particularly the more dynamic ones or web forms) are functioning as well as prime Drupal's cache since it's been cleared. These are some scripts that automate that process.

# Installation

These scripts are fairly specific to my setup. I've made a `setup.sh` script which _should_ install all necessary dependencies (via [homebrew](http://brew.sh) and python's `pip`) but it's untested.

# Usage

```sh
> # prime cache, ensure successful HTTP responses
> ./test-site
> # automated form testing
> ./test-course-reserves.py
> # add "--live" to these to test live site
> # copy these scripts into ~/bin (which I have on my path)
> ./cp.sh
```

# License

[Apache V2](https://www.apache.org/licenses/LICENSE-2.0)
