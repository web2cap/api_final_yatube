from django import template

register = template.Library()


@register.filter
def addclass(field, css):
    """The Addclass filter allows you to add CSS class to the template tag."""

    return field.as_widget(attrs={"class": css})
