from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.models import Orderable, Page


class DogImage(Orderable):
    page = ParentalKey("Dog", on_delete=models.CASCADE, related_name="images")
    image = models.ForeignKey("wagtailimages.Image", on_delete=models.CASCADE, related_name="+")
    # caption = models.CharField(blank=True, max_length=250)

    panels = [
        FieldPanel("image"),
        # FieldPanel('caption'),
    ]


class Dog(Page):
    dob = models.DateField("Date of Birth")
    # images = models.ManyToManyField("wagtailimages.Image", blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("dob"),
        InlinePanel("images", label="Images"),
        # MultipleChooserPanel('images', chooser_field_name="image"),
    ]
