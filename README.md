# Transcript to LaTeX pdf converter 

## This application can be found at www.SCUTranscript.com.
### Feel free to give me feedback or feature requests!

## Running Locally

Make sure you have Python [installed properly](http://install.python-guide.org). Also, install the [Heroku Toolbelt](https://toolbelt.heroku.com/) and Virtualenv.

```sh
$ git clone github.com/rsullivan00/transcript-to-latex.git
$ cd transcript-to-latex
$ virtualenv --no-site-packages --python=python3 venv
$ source venv/bin/activate
$ pip install -r requirements.txt --allow-all-external
$ foreman start web
```

Your app should now be running on [localhost:5000](http://localhost:5000/).


