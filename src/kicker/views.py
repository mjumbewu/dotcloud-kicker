from django.views.generic import TemplateView

class KickerView (TemplateView):
    template_name = 'kicker/kicker.html'

kicker_view = KickerView.as_view()
