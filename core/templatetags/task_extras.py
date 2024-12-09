from django import template

register = template.Library()

@register.filter
def status_color(status):
    colors = {
        'pending': 'badge-pending',
        'completed': 'badge-completed',
        'in-progress': 'badge-in-progress',
        'cancelled': 'badge-cancelled',
    }
    return colors.get(status.lower(), 'badge-secondary')
