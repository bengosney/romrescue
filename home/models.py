from django.db import models
from modelcluster.fields import ParentalKey
from wagtail import blocks
from wagtail.admin.panels import FieldPanel, FieldRowPanel, InlinePanel, MultiFieldPanel
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.contrib.forms.panels import FormSubmissionsPanel
from wagtail.fields import RichTextField, StreamField

from dogs.blocks import DogListBlock

from .blocks import FormBlock, SectionBlock, TitleBlock


class FormField(AbstractFormField):
    page = ParentalKey("HomePage", on_delete=models.CASCADE, related_name="form_fields")


class HomePage(AbstractEmailForm):
    max_count = 1

    content = StreamField(
        [
            (
                "Section",
                SectionBlock(
                    [
                        ("SiteTitle", TitleBlock()),
                        ("Paragraph", blocks.RichTextBlock()),
                        ("Dogs", DogListBlock()),
                        ("Form", FormBlock()),
                    ]
                ),
            ),
        ],
        use_json_field=True,
        blank=True,
    )
    thank_you_text = RichTextField(blank=True)
    submit_text = models.CharField(
        verbose_name="Submit button text",
        max_length=255,
        default="Submit",
        help_text="Text that will appear on the form's submit button",
    )

    content_panels = AbstractEmailForm.content_panels + [
        FormSubmissionsPanel(),
        FieldPanel("content"),
        MultiFieldPanel(
            [
                InlinePanel("form_fields", label="Form fields"),
                FieldPanel("submit_text"),
                FieldPanel("thank_you_text"),
            ]
        ),
        MultiFieldPanel(
            [
                FieldRowPanel(
                    [
                        FieldPanel("from_address", classname="col6"),
                        FieldPanel("to_address", classname="col6"),
                    ]
                ),
                FieldPanel("subject"),
            ],
            "Email",
        ),
    ]
