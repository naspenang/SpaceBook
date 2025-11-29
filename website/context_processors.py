# website/context_processors.py
from social_django.models import UserSocialAuth


def google_profile_picture(request):
    picture = None
    user = request.user

    if user.is_authenticated:
        try:
            social = user.social_auth.get(provider="google-oauth2")
            # This is where Google usually stores the avatar URL
            picture = social.extra_data.get("picture")
        except UserSocialAuth.DoesNotExist:
            picture = None
        except Exception:
            picture = None

    return {"google_picture": picture}
