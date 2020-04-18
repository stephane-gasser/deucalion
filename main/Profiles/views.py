from django.views.generic.list import ListView

class CreditLineView(ListView):
    def get_queryset(self):
        return self.request.user.get_profile().creditline_set.all()
        
        
