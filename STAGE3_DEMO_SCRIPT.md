# Stage 3 Demo Script

Target length: 5-10 minutes.

## 0:00-0:45 - Introduction

Hi, this is my CS348 Stage 3 demo for MusicLog.

MusicLog is a Django web application for tracking album reviews. The app lets users manage artists, genres, albums, and reviews. It also includes a report page where users can filter reviews by artist, genre, album, release year range, and rating range.

For the final deployment, my code is hosted on GitHub and the application is deployed on Vercel with a Neon Postgres database.

GitHub URL: `https://github.com/prathamcs/cs348-project`

Application URL: `<paste your Vercel URL here>`

## 0:45-1:45 - Application Demo

First, I will show the main application workflow.

On the home page, the app lists album reviews. Each review shows the album, artist, genre, year, rating, review text, and listened date.

Now I will add or update sample data. I can manage artists, albums, and genres from their own pages. For example, I can add an artist such as Tyler, the Creator or Jeff Buckley, create an album for that artist, and then add a review for that album.

After saving the review, it appears on the main review list. The list is sorted by the newest listened date first.

Next, I will open the Review Report page. This report lets me filter the review data by artist, genre, album, year range, and rating range. When I apply filters, the table updates, and the statistics section shows the total number of matching reviews and the average rating.

## 1:45-3:00 - SQL Injection Protection

Next, I will show how the application protects against SQL injection.

In `reviews/forms.py`, the app uses Django forms for all user input. The create and edit pages use `ModelForm` classes like `ReviewForm`, `ArtistForm`, `AlbumForm`, and `GenreForm`.

The report page uses `ReviewReportForm`. This form defines typed fields:

- `ModelChoiceField` for artist, genre, and album.
- `IntegerField` for release year filters.
- `DecimalField` for rating filters.

This means user input is validated and converted to Python objects before it is used in queries.

In `reviews/views.py`, the report view only reads values from `form.cleaned_data`. For example, it gets the selected artist, genre, album, minimum year, maximum year, minimum rating, and maximum rating from the validated form.

Then the code builds the report query using Django ORM filters, such as:

```python
reviews = reviews.filter(album__artist=artist)
reviews = reviews.filter(album__genre=genre)
reviews = reviews.filter(rating__gte=min_rating)
reviews = reviews.filter(rating__lte=max_rating)
```

The important point is that the app never concatenates raw user input into SQL strings. Django's ORM sends these values to the database as query parameters, so input is treated as data, not executable SQL.

For example, if a user typed something like `' OR 1=1 --` into a text field, Django would treat it as a string value. It would not become part of the SQL command.

In `reviews/models.py`, I also added validators for numeric fields. The album release year is restricted to a valid range, and the review rating is restricted between 0 and 5. That gives another layer of input validation before data is saved.

## 3:00-4:45 - Indexes

Next, I will discuss indexes.

The indexes are defined in `reviews/models.py`, and Django generated a migration for them in `reviews/migrations/0002...`.

First, `Artist.name` has `db_index=True`. This supports the Manage Artists page, where artists are ordered by name:

```python
Artist.objects.all().order_by("name")
```

This is useful because users expect artists to be shown alphabetically.

Second, the app has an index named `album_artist_year_idx` on `Album(artist, release_year)`. This supports the Review Report when a user filters by artist and release year range. For example, a report like "reviews for Tyler, the Creator albums between 2010 and 2020" benefits from this index.

Third, there is an index named `album_genre_year_idx` on `Album(genre, release_year)`. This supports reports filtered by genre and release year range, such as "rock albums released after 1990."

Fourth, there is an index named `album_title_idx` on `Album(title)`. This supports the Manage Albums page, where albums are ordered by title.

Fifth, there is an index named `review_rating_idx` on `Review(rating)`. This supports the Review Report rating filters:

```python
reviews.filter(rating__gte=min_rating)
reviews.filter(rating__lte=max_rating)
```

This is useful for reports like "show all reviews rated 4.0 or higher."

Sixth, there is an index named `review_album_rating_idx` on `Review(album, rating)`. This supports reports where the user filters by a specific album and a rating range at the same time.

Finally, there is an index named `review_listened_on_idx` on `Review(listened_on)`. This supports the main review list and report output, which order reviews by newest listened date first:

```python
.order_by("-listened_on", "-created_at")
```

These indexes are meaningful because they support the actual user-facing list, management pages, and report filters in the application.

## 4:45-6:15 - Transactions and Concurrency

Next, I will discuss transactions and concurrency.

Even though this is a small project, the deployed version can be accessed by multiple users at the same time. That means two users could try to update or delete the same review concurrently.

In `reviews/views.py`, write operations are wrapped in `transaction.atomic()`.

For example, when adding a review:

```python
with transaction.atomic():
    form.save()
```

This means the database operation is all-or-nothing. If the save succeeds, the transaction commits. If an error occurs, Django rolls back the transaction so the database is not left in a partial state.

For review edits and deletes, I also use `select_for_update()`:

```python
review = get_object_or_404(Review.objects.select_for_update(), id=review_id)
```

On Postgres, this creates a row-level lock inside the transaction. If two users try to edit or delete the same review at the same time, one transaction locks the row first, and the other transaction waits until the first one finishes.

The hosted app uses Neon Postgres. Postgres uses `READ COMMITTED` isolation by default. That is a reasonable isolation level for this project because it prevents dirty reads, while avoiding the overhead of fully serializable transactions.

So my concurrency strategy is:

- Use Postgres's default `READ COMMITTED` isolation.
- Wrap writes in `transaction.atomic()`.
- Use row-level locking with `select_for_update()` for review update and delete operations.

## 6:15-7:00 - AI Use

I also need to discuss how I used AI in the project.

I used AI as a development assistant. It helped me review the Stage 3 rubric, identify where the existing Django code already protected against SQL injection, add explicit indexes, add transaction blocks, and organize the demo explanation.

I also used AI to help create the Stage 3 demo guide and this script.

The final responsibility was still mine. I reviewed the code changes, generated migrations, ran Django checks and tests locally, pushed the code to GitHub, and deployed the app using Vercel and Neon.

## 7:00-8:00 - Deployment Proof

Finally, I will show that the app is deployed.

The live app is running on Vercel, and the database is hosted on Neon Postgres.

To prove that the live app and database are connected, I will add or edit a review on the deployed website. Then I will open the Review Report page and show that the report reflects the new or updated data.

This demonstrates that the deployed app is not just static code. It is connected to a hosted database and can perform create, update, delete, and report operations.

That concludes my Stage 3 demo.
