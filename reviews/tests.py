from django.test import TestCase
from django.urls import reverse

from .models import Album, Artist, Genre


class EntityCrudTests(TestCase):
    def setUp(self):
        self.artist = Artist.objects.create(name="Initial Artist")
        self.genre = Genre.objects.create(name="Rock")
        self.album = Album.objects.create(
            title="First Album",
            artist=self.artist,
            genre=self.genre,
            release_year=2001,
        )

    def test_add_artist(self):
        response = self.client.post(reverse("add_artist"), {"name": "New Artist"})

        self.assertRedirects(response, reverse("manage_artists"))
        self.assertTrue(Artist.objects.filter(name="New Artist").exists())

    def test_edit_artist(self):
        response = self.client.post(
            reverse("edit_artist", args=[self.artist.id]),
            {"name": "Updated Artist"},
        )

        self.assertRedirects(response, reverse("manage_artists"))
        self.artist.refresh_from_db()
        self.assertEqual(self.artist.name, "Updated Artist")

    def test_delete_artist(self):
        response = self.client.post(reverse("delete_artist", args=[self.artist.id]))

        self.assertRedirects(response, reverse("manage_artists"))
        self.assertFalse(Artist.objects.filter(id=self.artist.id).exists())

    def test_add_genre(self):
        response = self.client.post(reverse("add_genre"), {"name": "Jazz"})

        self.assertRedirects(response, reverse("manage_genres"))
        self.assertTrue(Genre.objects.filter(name="Jazz").exists())

    def test_edit_genre(self):
        response = self.client.post(
            reverse("edit_genre", args=[self.genre.id]),
            {"name": "Alternative"},
        )

        self.assertRedirects(response, reverse("manage_genres"))
        self.genre.refresh_from_db()
        self.assertEqual(self.genre.name, "Alternative")

    def test_delete_genre(self):
        other_artist = Artist.objects.create(name="Second Artist")
        other_genre = Genre.objects.create(name="Pop")
        genre = Genre.objects.create(name="Electronic")
        Album.objects.create(
            title="Standalone Album",
            artist=other_artist,
            genre=other_genre,
            release_year=2005,
        )

        response = self.client.post(reverse("delete_genre", args=[genre.id]))

        self.assertRedirects(response, reverse("manage_genres"))
        self.assertFalse(Genre.objects.filter(id=genre.id).exists())

    def test_add_album(self):
        other_artist = Artist.objects.create(name="Another Artist")
        other_genre = Genre.objects.create(name="Hip-Hop")

        response = self.client.post(reverse("add_album"), {
            "title": "Second Album",
            "artist": other_artist.id,
            "genre": other_genre.id,
            "release_year": 2023,
        })

        self.assertRedirects(response, reverse("manage_albums"))
        self.assertTrue(Album.objects.filter(title="Second Album").exists())

    def test_edit_album(self):
        other_artist = Artist.objects.create(name="Edited Artist")
        other_genre = Genre.objects.create(name="Indie")

        response = self.client.post(reverse("edit_album", args=[self.album.id]), {
            "title": "Renamed Album",
            "artist": other_artist.id,
            "genre": other_genre.id,
            "release_year": 2010,
        })

        self.assertRedirects(response, reverse("manage_albums"))
        self.album.refresh_from_db()
        self.assertEqual(self.album.title, "Renamed Album")
        self.assertEqual(self.album.artist, other_artist)
        self.assertEqual(self.album.genre, other_genre)
        self.assertEqual(self.album.release_year, 2010)

    def test_delete_album(self):
        response = self.client.post(reverse("delete_album", args=[self.album.id]))

        self.assertRedirects(response, reverse("manage_albums"))
        self.assertFalse(Album.objects.filter(id=self.album.id).exists())

    def test_management_pages_render(self):
        response = self.client.get(reverse("manage_artists"))
        self.assertContains(response, "Manage Artists")

        response = self.client.get(reverse("manage_albums"))
        self.assertContains(response, "Manage Albums")

        response = self.client.get(reverse("manage_genres"))
        self.assertContains(response, "Manage Genres")
