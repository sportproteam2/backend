import firebase_admin
import os

from firebase_admin import credentials
from django.conf import settings

cred = credentials.Certificate(
    os.path.join(settings.BASE_DIR, "sportpro-c5b31-firebase-adminsdk-rvvh7-1a28b7dc64.json"))
firebase_admin.initialize_app(cred)