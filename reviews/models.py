from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Artist(models.Model):
    name = models.CharField(max_length=100, db_index=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Album(models.Model):
    title = models.CharField(max_length=150)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    release_year = models.IntegerField(
        validators=[MinValueValidator(1900), MaxValueValidator(2100)]
    )

    class Meta:
        indexes = [
            models.Index(fields=["artist", "release_year"], name="album_artist_year_idx"),
            models.Index(fields=["genre", "release_year"], name="album_genre_year_idx"),
            models.Index(fields=["title"], name="album_title_idx"),
        ]

    def __str__(self):
        return f"{self.title} ({self.artist.name})"


class Review(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    rating = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
    )
    review_text = models.TextField()
    listened_on = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["rating"], name="review_rating_idx"),
            models.Index(fields=["album", "rating"], name="review_album_rating_idx"),
            models.Index(fields=["listened_on"], name="review_listened_on_idx"),
        ]

    def __str__(self):
        return f"{self.album.title} - {self.rating}"
