from django import template

register = template.Library()

@register.simple_tag
def my_custom_tag():
    return "Hello from form_tags!"

# Adding the missing filter for Bootstrap form styling
@register.filter(name='addclass')
def addclass(field, css_class):
    return field.as_widget(attrs={"class": css_class})