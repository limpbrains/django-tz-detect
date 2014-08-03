from django.utils import timezone

from tz_detect.utilities import offset_to_timezone


class TimezoneMiddleware(object):
    def process_request(self, request):
        if request.user.is_authenticated():
            profile = request.user.get_profile()
            if profile.timezone:
                timezone.activate(profile.timezone)
                request.timezone_active = True
                return

        tz = request.session.get('detected_tz')
        if tz:
            # `request.timezone_active` is used in the template
            # tag to detect if the timezone has been activated
            tz = offset_to_timezone(tz)
            request.timezone_active = True
            timezone.activate(tz)
        else:
            timezone.deactivate()
