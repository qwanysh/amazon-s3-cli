# amazon-s3-cli
Python CLI for Amazon S3

#### Setup
```bash
# install dependencies
pipenv install

cp .env.example .env
# configure .env

# activate shell
pipenv shell
```

#### Usage
```bash
# help
python main.py --help

# upload
python main.py upload <file-to-upload>

# upload with custom key
python main.py upload <file-to-upload> -k <custom-key>
```
