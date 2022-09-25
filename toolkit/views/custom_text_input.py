from django.forms.widgets import Input
import os


class CustomTextInput(Input):
    cwd = os.getcwd()
    template_name = os.path.join(cwd, "toolkit\\templates\\custom_text_input.html")

    def __init__(self, attrs=None):
        self.placeholder = None
        if attrs is not None:
            attrs = attrs.copy()
            self.placeholder = attrs.pop("placeholder", None)
        super().__init__(attrs)

    def render(self, name, value, attrs=None, renderer=None):
        """Render the widget as an HTML string."""
        context = self.get_context(name, value, attrs)
        return self._render(self.template_name, context, renderer)

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context["widget"]["placeholder"] = self.placeholder
        return context
