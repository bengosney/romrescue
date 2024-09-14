from wagtail import blocks

from .models import Dog


class DogListBlock(blocks.StaticBlock):
    class Meta:
        template = "dogs/blocks/dog_list_block.html"

    title = blocks.CharBlock(required=True)

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context)
        page = context.get("page", None)
        if page:
            context["dogs"] = Dog.objects.descendant_of(page).live()  # type: ignore

        return context
