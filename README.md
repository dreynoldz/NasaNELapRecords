# NasaNE LapRecords
Nasa North East site rebuild


### Initializing Repo
```powershell
git clone https://github.com/dreynoldz/NasaNELapRecords.git
cd <cloned dir>
python3 -m venv env
.\env\Scripts\activate
pip install -r .\requirements.txt
```
### Running the app
```powershell
python3 .\manage.py --help

Usage: manage.py [OPTIONS] COMMAND [ARGS]...

Options:
  --version  Show the flask version
  --help     Show this message and exit.

Commands:
  cov           Runs the unit tests with coverage.
  create_admin  Creates the admin user.
  create_data   Creates sample data.
  create_db
  db            Perform database migrations.
  drop_db       Drops the db tables.
  run           Runs a development server.
  shell         Runs a shell in the app context.
  test          Runs the unit tests without test coverage.
```
