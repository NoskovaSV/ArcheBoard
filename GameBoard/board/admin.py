from django.contrib import admin
from .models import User, Ad, Category, Feedback
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms

admin.site.register(User)
admin.site.register(Ad)
admin.site.register(Category)
admin.site.register(Feedback)

class AdAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())
    class Meta:
        model = Ad
        fields = '__all__'


class AdAdmin(admin.ModelAdmin):
    form=AdAdminForm
