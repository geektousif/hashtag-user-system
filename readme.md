# How to Run

1. First clone the repo and then create a virtual environment inside the root folder

   ```bash
   python -m venv env
   ```

2. Activate the environment

   ```bash
   env/scripts/activate
   ```

3. Migrate the database and other things.

   ```bash
   python manage.py makemigrations
   ```

   ```bash
   python manage.py migrate
   ```

4. Run the Server
   ```bash
   python manage.py createsuperuser
   ```

### Access the Postman API Documentation [here](https://documenter.getpostman.com/view/13701358/2s8ZDR75n5)
