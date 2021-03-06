from django import forms
from django.core.exceptions import ValidationError

from blogs.models import Post, Blog

from django.utils.translation import ugettext as _

from dTBack import settings


class PostForm(forms.ModelForm):

    blog_id = forms.CharField(
        widget=forms.Select,
        label='Blog'
    )

    def __init__(self, *args, **kwargs):
        if kwargs.get("user"):
            user = kwargs.pop("user")
        super(PostForm, self).__init__(*args, **kwargs)
        if 'user' in locals() and not user.is_anonymous():
            self.__load_blog_user(user)
        else:
#Solución fea y de emergencia, pero no quiero que puedan crear post asociados a blogs de usuarios que no corresponden
            raise ValidationError(_("Debe estar conectado"))

    class Meta:
        model = Post
        fields = ("title", "abstract", "body", "attachment", "attachment_description", "categories", "date_pub")

#Estas etiquetas deben traducirse, pueden crearse las claves la primera vez y luego descomentarlas cada vez que se compile
        labels = {
            "title": "Título",
            "abstract": "Resumen",
            "body": "Texto",
            "attachment": "Media",
            "attachment_description": "Descripción de Media",
            "categories": "Categorías",
            "date_pub": "Fecha de publicación"
        }

    def __load_blog_user(self, user):
        blogs = Blog.objects.filter(owner=user.id)
        dBlog = [('', '------')]
        for blog in blogs:
            t = (blog.id, blog.__str__())
            dBlog.append(t)

        tBlog = tuple(dBlog)

        self.fields["blog_id"].widget.choices = tBlog
        return


class BlogForm(forms.ModelForm):

    class Meta:
        model = Blog
        fields = ("name", "description")
        # Estas etiquetas deben traducirse, pueden crearse las claves la primera vez y luego descomentarlas cada vez que se compile
        labels = {
            "name": "Nombre",
            "description": "Descripción"
        }



