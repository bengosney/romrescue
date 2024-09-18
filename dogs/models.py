from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.fields import RichTextField
from wagtail.models import Orderable, Page


class DogImage(Orderable):
    page = ParentalKey("Dog", on_delete=models.CASCADE, related_name="images")
    image = models.ForeignKey("wagtailimages.Image", on_delete=models.CASCADE, related_name="+")

    panels = [
        FieldPanel("image"),
    ]


class Dog(Page):
    body = RichTextField()

    content_panels = Page.content_panels + [
        FieldPanel("body"),
        InlinePanel("images", label="Images"),
    ]
