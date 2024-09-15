from wagtail import blocks
from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField
from wagtail.models import Page

from dogs.blocks import DogListBlock

from .blocks import SectionBlock, TitleBlock


class HomePage(Page):
    content = StreamField(
        [
            (
                "Section",
                SectionBlock(
                    [
                        ("SiteTitle", TitleBlock()),
                        ("Paragraph", blocks.RichTextBlock()),
                        ("Dogs", DogListBlock()),
                    ]
                ),
            ),
        ],
        use_json_field=True,
        blank=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("content"),
    ]
