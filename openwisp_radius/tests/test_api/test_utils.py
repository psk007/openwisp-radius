from rest_framework.exceptions import APIException

from ... import settings as app_settings
from ...api.utils import is_registration_enabled
from ...utils import load_model
from ..mixins import BaseTestCase

OrganizationRadiusSettings = load_model('OrganizationRadiusSettings')


class TestUtils(BaseTestCase):
    def test_is_registration_enabled(self):
        org = self._create_org()
        OrganizationRadiusSettings.objects.create(organization=org)

        with self.subTest('Test registration enabled set to True'):
            org.radius_settings.registration_enabled = True
            self.assertEqual(is_registration_enabled(org), True)

        with self.subTest('Test registration enabled set to False'):
            org.radius_settings.registration_enabled = False
            self.assertEqual(is_registration_enabled(org), False)

        with self.subTest('Test registration enabled set to None'):
            org.radius_settings.registration_enabled = None
            self.assertEqual(
                is_registration_enabled(org), app_settings.REGISTRATION_API_ENABLED,
            )

        with self.subTest('Test related radius setting does not exist'):
            org.radius_settings = None
            with self.assertRaises(APIException) as context_manager:
                is_registration_enabled(org)
            self.assertEqual(
                str(context_manager.exception),
                'Could not complete operation because of an internal misconfiguration',
            )
