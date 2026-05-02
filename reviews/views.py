from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from django.db.models import Avg
from .models import Review, Artist, Album, Genre
from .forms import (
    ReviewForm,
    ReviewReportForm,
    ArtistForm,
    AlbumForm,
    GenreForm,
)


def review_list(request):
    reviews = Review.objects.select_related(
        "album", "album__artist", "album__genre"
    ).order_by("-listened_on", "-created_at")
    return render(request, "reviews/review_list.html", {"reviews": reviews})


def manage_artists(request):
    artists = Artist.objects.all().order_by("name")
    return render(request, "reviews/entity_list.html", {
        "objects": artists,
        "entity_name": "Artists",
        "add_url": "add_artist",
        "edit_url": "edit_artist",
        "delete_url": "delete_artist",
        "display_attr": "name",
    })


def manage_albums(request):
    albums = Album.objects.select_related("artist", "genre").all().order_by("title")
    return render(request, "reviews/entity_list.html", {
        "objects": albums,
        "entity_name": "Albums",
        "add_url": "add_album",
        "edit_url": "edit_album",
        "delete_url": "delete_album",
        "display_attr": "title",
    })


def manage_genres(request):
    genres = Genre.objects.all().order_by("name")
    return render(request, "reviews/entity_list.html", {
        "objects": genres,
        "entity_name": "Genres",
        "add_url": "add_genre",
        "edit_url": "edit_genre",
        "delete_url": "delete_genre",
        "display_attr": "name",
    })


def add_artist(request):
    return _save_entity(
        request=request,
        form_class=ArtistForm,
        title="Add Artist",
        redirect_name="manage_artists",
    )


def edit_artist(request, artist_id):
    artist = get_object_or_404(Artist, id=artist_id)
    return _save_entity(
        request=request,
        form_class=ArtistForm,
        title="Edit Artist",
        redirect_name="manage_artists",
        instance=artist,
    )


def delete_artist(request, artist_id):
    artist = get_object_or_404(Artist, id=artist_id)
    return _delete_entity(
        request=request,
        obj=artist,
        label=artist.name,
        redirect_name="manage_artists",
        entity_label="artist",
    )


def add_album(request):
    return _save_entity(
        request=request,
        form_class=AlbumForm,
        title="Add Album",
        redirect_name="manage_albums",
    )


def edit_album(request, album_id):
    album = get_object_or_404(Album, id=album_id)
    return _save_entity(
        request=request,
        form_class=AlbumForm,
        title="Edit Album",
        redirect_name="manage_albums",
        instance=album,
    )


def delete_album(request, album_id):
    album = get_object_or_404(Album, id=album_id)
    return _delete_entity(
        request=request,
        obj=album,
        label=str(album),
        redirect_name="manage_albums",
        entity_label="album",
    )


def add_genre(request):
    return _save_entity(
        request=request,
        form_class=GenreForm,
        title="Add Genre",
        redirect_name="manage_genres",
    )


def edit_genre(request, genre_id):
    genre = get_object_or_404(Genre, id=genre_id)
    return _save_entity(
        request=request,
        form_class=GenreForm,
        title="Edit Genre",
        redirect_name="manage_genres",
        instance=genre,
    )


def delete_genre(request, genre_id):
    genre = get_object_or_404(Genre, id=genre_id)
    return _delete_entity(
        request=request,
        obj=genre,
        label=genre.name,
        redirect_name="manage_genres",
        entity_label="genre",
    )


def add_review(request):
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                form.save()
            return redirect("review_list")
    else:
        form = ReviewForm()
    return render(request, "reviews/review_form.html", {
        "form": form,
        "title": "Add Review",
        "cancel_url": "review_list",
    })


def edit_review(request, review_id):
    if request.method == "POST":
        with transaction.atomic():
            review = get_object_or_404(Review.objects.select_for_update(), id=review_id)
            form = ReviewForm(request.POST, instance=review)
            if form.is_valid():
                form.save()
                return redirect("review_list")
    else:
        review = get_object_or_404(Review, id=review_id)
        form = ReviewForm(instance=review)
    return render(request, "reviews/review_form.html", {
        "form": form,
        "title": "Edit Review",
        "cancel_url": "review_list",
    })


def delete_review(request, review_id):
    if request.method == "POST":
        with transaction.atomic():
            review = get_object_or_404(Review.objects.select_for_update(), id=review_id)
            review.delete()
        return redirect("review_list")
    review = get_object_or_404(Review, id=review_id)
    return render(request, "reviews/review_delete.html", {"review": review})


def review_report(request):
    reviews = Review.objects.select_related(
        "album", "album__artist", "album__genre"
    ).order_by("-listened_on", "-created_at")
    form = ReviewReportForm(request.GET or None)

    if form.is_valid():
        artist = form.cleaned_data.get("artist")
        genre = form.cleaned_data.get("genre")
        album = form.cleaned_data.get("album")
        min_year = form.cleaned_data.get("min_year")
        max_year = form.cleaned_data.get("max_year")
        min_rating = form.cleaned_data.get("min_rating")
        max_rating = form.cleaned_data.get("max_rating")

        if artist:
            reviews = reviews.filter(album__artist=artist)
        if genre:
            reviews = reviews.filter(album__genre=genre)
        if album:
            reviews = reviews.filter(album=album)
        if min_year is not None:
            reviews = reviews.filter(album__release_year__gte=min_year)
        if max_year is not None:
            reviews = reviews.filter(album__release_year__lte=max_year)
        if min_rating is not None:
            reviews = reviews.filter(rating__gte=min_rating)
        if max_rating is not None:
            reviews = reviews.filter(rating__lte=max_rating)

    stats = reviews.aggregate(average_rating=Avg("rating"))

    return render(request, "reviews/report.html", {
        "form": form,
        "reviews": reviews,
        "stats": stats,
        "count": reviews.count(),
    })


def _save_entity(request, form_class, title, redirect_name, instance=None):
    if request.method == "POST":
        form = form_class(request.POST, instance=instance)
        if form.is_valid():
            with transaction.atomic():
                form.save()
            return redirect(redirect_name)
    else:
        form = form_class(instance=instance)

    return render(request, "reviews/review_form.html", {
        "form": form,
        "title": title,
        "cancel_url": redirect_name,
    })


def _delete_entity(request, obj, label, redirect_name, entity_label):
    if request.method == "POST":
        with transaction.atomic():
            obj.delete()
        return redirect(redirect_name)

    return render(request, "reviews/entity_delete.html", {
        "object_label": label,
        "entity_label": entity_label,
        "cancel_url": redirect_name,
    })
