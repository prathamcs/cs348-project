# Deploying MusicLog to Vercel

Vercel can host the Django app. For Stage 3 extra credit, use a hosted Postgres database too, such as Neon from the Vercel Marketplace. Do not use the local `db.sqlite3` file for the deployed app.

## 1. Push the Code

The app code should be on GitHub:

```bash
git push origin main
```

## 2. Create the Vercel Project

1. Go to Vercel.
2. Import the GitHub repository.
3. Select the `main` branch.
4. Deploy the project.

Vercel detects Django projects from `manage.py` and the WSGI settings.

## 3. Add Postgres

1. In the Vercel project dashboard, open Storage or Marketplace.
2. Add a Postgres database provider, such as Neon.
3. Connect it to this Vercel project.
4. Confirm Vercel added a database connection variable such as `DATABASE_URL` or `POSTGRES_URL`.

The Django settings support both names.

## 4. Add Environment Variables

In the Vercel project dashboard, add these variables for Production:

```text
DJANGO_DEBUG=0
DJANGO_SECRET_KEY=<generated-secret-key>
DATABASE_URL=<postgres-connection-string>
```

If Vercel provides `POSTGRES_URL` instead of `DATABASE_URL`, that is fine.

To generate a Django secret locally:

```bash
.venv/bin/python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## 5. Run Migrations on the Hosted Database

After the hosted Postgres database exists, run migrations against it from your machine:

```bash
source .venv/bin/activate
pip install -r requirements.txt
DATABASE_URL="<postgres-connection-string>" DJANGO_DEBUG=0 python manage.py migrate
```

Optional: create an admin user on the hosted database:

```bash
DATABASE_URL="<postgres-connection-string>" DJANGO_DEBUG=0 python manage.py createsuperuser
```

## 6. Deploy Updates

If the GitHub repo is connected to Vercel, each push to `main` can trigger a new deployment:

```bash
git add .
git commit -m "Describe change"
git push origin main
```

If using the Vercel CLI:

```bash
vercel --prod
```

## 7. Submission

Submit:

- GitHub URL: `https://github.com/prathamcs/cs348-project`
- App URL: the production Vercel URL, usually `https://<project-name>.vercel.app`

Keep the Vercel app and hosted database running through the grading window, then delete them if you do not want ongoing charges.
