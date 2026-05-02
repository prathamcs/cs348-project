# Stage 3 Demo Guide

Use this as the outline for the 5-10 minute recording.

## 1. Application Overview

- Project: MusicLog, a Django application for tracking album reviews.
- Main user actions:
  - Add, edit, and delete artists, genres, albums, and reviews.
  - Generate a review report filtered by artist, genre, album, release year range, and rating range.

## 2. SQL Injection Protection

Show these files:

- `reviews/forms.py`
  - `ReviewForm`, `ArtistForm`, `GenreForm`, and `AlbumForm` are Django forms.
  - `ReviewReportForm` validates report filter input and exposes values through `cleaned_data`.
- `reviews/views.py`
  - `review_report()` reads only validated values from `form.cleaned_data`.
  - The query is built with Django ORM calls such as `reviews.filter(album__artist=artist)` and `reviews.filter(rating__gte=min_rating)`.
- `reviews/models.py`
  - `release_year` and `rating` have numeric validators to reject invalid ranges before database writes.

Talking points:

- The app does not build SQL strings from user input.
- Django ORM queries are parameterized by the database adapter, so values are bound separately from SQL text.
- Report filters use typed Django form fields:
  - `ModelChoiceField` for artist, genre, and album.
  - `IntegerField` for year filters.
  - `DecimalField` for rating filters.
- Django templates escape output by default, so review text is displayed safely in the UI.

Example attack to mention:

- If a user enters text like `' OR 1=1 --` into a text field, it is stored as a value, not executed as SQL.

## 3. Indexes

Show `reviews/models.py`.

### Artist name index

- Code: `Artist.name` has `db_index=True`.
- Supports: `manage_artists()` in `reviews/views.py`, which runs `Artist.objects.all().order_by("name")`.
- Feature: Manage Artists page.
- Justification: users view artists alphabetically, so the database can use the index for sorting.

### Album artist and release year index

- Code: `album_artist_year_idx` on `Album(artist, release_year)`.
- Supports: `review_report()` filters by artist and release year range.
- Feature: Review Report.
- Example query path:
  - `reviews.filter(album__artist=artist)`
  - `reviews.filter(album__release_year__gte=min_year)`
  - `reviews.filter(album__release_year__lte=max_year)`
- Justification: this helps reports like "reviews for this artist between 2010 and 2020."

### Album genre and release year index

- Code: `album_genre_year_idx` on `Album(genre, release_year)`.
- Supports: `review_report()` filters by genre and release year range.
- Feature: Review Report.
- Example query path:
  - `reviews.filter(album__genre=genre)`
  - release year min/max filters.
- Justification: this helps reports like "hip-hop albums released after 2015."

### Album title index

- Code: `album_title_idx` on `Album(title)`.
- Supports: `manage_albums()` in `reviews/views.py`, which runs `Album.objects.select_related(...).order_by("title")`.
- Feature: Manage Albums page.
- Justification: users view albums alphabetically, so this supports repeated title sorting.

### Review rating index

- Code: `review_rating_idx` on `Review(rating)`.
- Supports: `review_report()` filters by `min_rating` and `max_rating`.
- Feature: Review Report.
- Example query path:
  - `reviews.filter(rating__gte=min_rating)`
  - `reviews.filter(rating__lte=max_rating)`
- Justification: rating range reports are core report filters.

### Review album and rating index

- Code: `review_album_rating_idx` on `Review(album, rating)`.
- Supports: `review_report()` when a user filters by album and rating range together.
- Feature: Review Report.
- Example query path:
  - `reviews.filter(album=album)`
  - rating min/max filters.
- Justification: this is useful for reports scoped to one album and rating threshold.

### Review listened date index

- Code: `review_listened_on_idx` on `Review(listened_on)`.
- Supports: `review_list()` and `review_report()`, which order reviews by newest listened date first.
- Feature: Review List and Review Report.
- Example query path:
  - `Review.objects.select_related(...).order_by("-listened_on", "-created_at")`
- Justification: the newest listened albums appear first in both the normal list and report output.

Note:

- Django also creates indexes for foreign keys by default, including `Album.artist`, `Album.genre`, and `Review.album`.

## 4. Transactions and Isolation

Show `reviews/views.py`.

Code to show:

- `transaction.atomic()` around create, update, and delete operations.
- `select_for_update()` in `edit_review()` and `delete_review()` POST paths.

Talking points:

- Django runs in autocommit mode by default.
- For write operations, the app now uses explicit `transaction.atomic()` blocks so each create, edit, or delete commits as a single unit.
- For review updates and deletes, `select_for_update()` expresses row-level locking for databases that support it, such as PostgreSQL.
- This makes one conflicting update wait while another transaction owns the row lock.
- SQLite has limited isolation and does not support row-level `SELECT FOR UPDATE` locking the same way PostgreSQL does. If deployed on PostgreSQL, the same code would use the database's row locks.

Isolation level:

- Local development uses SQLite's default isolation behavior through Django.
- For a multi-user production version, a reasonable choice is the database default `READ COMMITTED` isolation level with row locks for conflicting writes. This avoids dirty reads and keeps write conflicts controlled without the overhead of serializing every transaction.

## 5. AI Use

Discuss this honestly:

- AI assistance was used to review the Stage 3 requirements, identify where the existing Django code already satisfied SQL injection protection, and add explicit indexes and transaction blocks.
- AI also helped draft this demo guide and organize the rubric talking points.
- Final responsibility stayed with the developer: code was reviewed, migrations were generated, and Django checks/tests were run locally.

## 6. GitHub and Deployment

Required submission:

- GitHub code URL: `<paste your GitHub repository URL here>`
- Application URL if deployed: `<paste live URL here, or say not deployed>`

Extra credit:

- If deploying, record the live URL working during the grading window.
- In the demo, add/edit/delete a record and show that the report reflects the changed data.
- Delete cloud resources after grading.
