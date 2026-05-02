from django.urls import path
from . import views

urlpatterns = [
    path("", views.review_list, name="review_list"),
    path("add/", views.add_review, name="add_review"),
    path("edit/<int:review_id>/", views.edit_review, name="edit_review"),
    path("delete/<int:review_id>/", views.delete_review, name="delete_review"),
    path("report/", views.review_report, name="review_report"),
    path("artists/", views.manage_artists, name="manage_artists"),
    path("artists/add/", views.add_artist, name="add_artist"),
    path("artists/edit/<int:artist_id>/", views.edit_artist, name="edit_artist"),
    path("artists/delete/<int:artist_id>/", views.delete_artist, name="delete_artist"),
    path("albums/", views.manage_albums, name="manage_albums"),
    path("albums/add/", views.add_album, name="add_album"),
    path("albums/edit/<int:album_id>/", views.edit_album, name="edit_album"),
    path("albums/delete/<int:album_id>/", views.delete_album, name="delete_album"),
    path("genres/", views.manage_genres, name="manage_genres"),
    path("genres/add/", views.add_genre, name="add_genre"),
    path("genres/edit/<int:genre_id>/", views.edit_genre, name="edit_genre"),
    path("genres/delete/<int:genre_id>/", views.delete_genre, name="delete_genre"),
]
