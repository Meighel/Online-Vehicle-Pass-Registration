from .models import SiteVisit
from django.utils.deprecation import MiddlewareMixin

class VisitorTrackingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if not request.session.session_key:
            request.session.create()
            
        session_key = request.session.session_key
        
        if not SiteVisit.objects.filter(session_key=session_key).exists():
            SiteVisit.objects.create(session_key=session_key,
                                     ip_address=self.get_client_ip(request),
                                     user_agent=request.META.get('HTTP_USER_AGENT', '')
                                     )      
            
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
