from wagtail import blocks


class SectionBlock(blocks.StructBlock):
    navigation_title = blocks.CharBlock(required=True)
    body = blocks.StreamBlock([])

    class Meta:
        template = "home/blocks/section_block.html"

    def __init__(self, local_blocks=None, search_index=True, **kwargs):
        super().__init__(None, search_index, **kwargs)

        if local_blocks:
            body = blocks.StreamBlock(local_blocks)
            body.set_name("body")
            self.child_blocks["body"] = body


class TitleBlock(blocks.StaticBlock):
    class Meta:
        template = "home/blocks/title_block.html"


class FormBlock(blocks.StructBlock):
    class Meta:
        template = "home/blocks/form.html"
        icon = "form"
