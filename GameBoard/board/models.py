from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField

class User(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    personal_email = models.EmailField(max_length=254)


class Ad(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ads")
    categories = models.ForeignKey('Category',null=True,on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = RichTextField(blank=True, null=True)
    creation_date = models.DateTimeField(auto_now_add=True)

class Category(models.Model):
    T = "tanks"
    H = "heals"
    D="DD"
    M="merchants"
    G="gildmasters"
    Q="questgivers"
    S="smiths"
    L="leatherworkers"
    P="potioncookers"
    SM="spellmasters"
    choices = ((T, "Танки"), (H, "Хилы"), (D, "ДД"), (M, "Торговцы"), (G, "Гилдмастеры"),(Q, "Квестгиверы"),
               (S, "Кузнецы"), (L, "Кожевники"), (P, "Зельевары"), (SM, "Мастера заклинаний"))
    choice_field = models.CharField(max_length=255, choices=choices, default="tanks")


class Feedback(models.Model):
    advert = models.ForeignKey(Ad, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="feedback")
    text = models.TextField(max_length=1024)
    created_at = models.DateTimeField(auto_now_add=True)

