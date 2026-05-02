from django import forms
from .models import Review, Artist, Genre, Album


class ArtistForm(forms.ModelForm):
    class Meta:
        model = Artist
        fields = ["name"]


class GenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = ["name"]


class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ["title", "artist", "genre", "release_year"]


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["album", "rating", "review_text", "listened_on"]
        widgets = {
            "listened_on": forms.DateInput(attrs={"type": "date"})
        }


class ReviewReportForm(forms.Form):
    artist = forms.ModelChoiceField(
        queryset=Artist.objects.all(),
        required=False,
        empty_label="All Artists"
    )
    genre = forms.ModelChoiceField(
        queryset=Genre.objects.all(),
        required=False,
        empty_label="All Genres"
    )
    album = forms.ModelChoiceField(
        queryset=Album.objects.all(),
        required=False,
        empty_label="All Albums"
    )
    min_year = forms.IntegerField(required=False)
    max_year = forms.IntegerField(required=False)
    min_rating = forms.DecimalField(required=False, decimal_places=1, max_digits=2)
    max_rating = forms.DecimalField(required=False, decimal_places=1, max_digits=2)
