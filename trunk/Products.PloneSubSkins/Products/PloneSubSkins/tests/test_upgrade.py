import unittest
from base import IntegrationTestCase

class UpgrateTest(IntegrationTestCase):
    def test_upgrade_step_3_1__to__3_2(self):
        setup = self.portal.portal_setup
        profile_id = u'Products.PloneSubSkins:default'
        # We fake a 3.1 version (it had version.txt but no metadata.xml)
        self.portal.portal_quickinstaller._getOb('PloneSubSkins').installedversion = "3.1"
        setup._profile_upgrade_versions[profile_id] = 'unknown'
        upgrade_steps = setup.listUpgrades(profile_id)
        # And we should get at least one upgrade step
        self.assertTrue(len(upgrade_steps)>0)


def test_suite():
    return unittest.TestSuite([
            unittest.makeSuite(UpgrateTest),
        ])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
