## Codex

### Installation

These installation instructions assume some basic knowledge of Django.

- Clone the repo
- Create a virtualenv for the project if you want
- Copy `local_settings_sample.py` to `local_settings.py` and edit to taste (and make sure you put something in `SECRET_KEY`)
- `pip install -r requirements.txt`
- `./manage.py migrate`
- `./manage.py createsuperuser`
- `./manage.py runserver 8001`

### Dropbox Integration

1. Go to the [Dropbox create app page](https://www.dropbox.com/developers/apps/create)
2. Choose `Drop-ins app`
3. Type in an app name and click `Create app` (the app name needs to be unique among all Dropbox apps)
4. Enter the drop-ins domains you plan to use (including `127.0.0.1` and `localhost` if you're developing locally)
5. Copy the app key into `local_settings.py` under `INTEGRATIONS.dropbox.key`.
