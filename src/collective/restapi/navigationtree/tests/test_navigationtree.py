# -*- coding: utf-8 -*-
from collective.restapi.navigationtree.testing import CRN_AT_FUNCTIONAL_TESTING
from collective.restapi.navigationtree.testing import CRN_DX_FUNCTIONAL_TESTING
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.app.testing import TEST_USER_ID
from plone.restapi.testing import RelativeSession

import transaction
import unittest


class NavigationBase(object):

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.portal_url = self.portal.absolute_url()
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

        self.api_session = RelativeSession(self.portal_url)
        self.api_session.headers.update({'Accept': 'application/json'})
        self.api_session.auth = (SITE_OWNER_NAME, SITE_OWNER_PASSWORD)

        self.folder = api.content.create(
            container=self.portal, type=u'Folder',
            id=u'folder',
            title=u'Some Folder')
        api.content.create(
            container=self.folder, type=u'Document',
            id=u'doc1',
            title=u'A document')
        transaction.commit()

    def test_navigation(self):
        response = self.api_session.get('/folder/@navigationtree')

        self.assertEqual(response.status_code, 200)
        self.maxDiff = None
        self.assertEqual(
            response.json(),
            {
                u'@id': u'http://localhost:55001/plone/folder/@navigationtree',
                u'items': [
                    {
                        u'title': u'Home',
                        u'description': u'',
                        u'items': u'',
                        u'@id': u'http://localhost:55001/plone',
                    },
                    {
                        u'title': u'folder-0',
                        u'description': u'',
                        u'items': [],
                        u'@id': u'http://localhost:55001/plone/folder-0',
                    },
                    {
                        u'title': u'folder-1',
                        u'description': u'',
                        u'items': [],
                        u'@id': u'http://localhost:55001/plone/folder-1',
                    },
                    {
                        u'title': u'Some Folder',
                        u'description': u'',
                        u'@id': u'http://localhost:55001/plone/folder',
                        u'items': [
                            {
                                u'title': u'A document',
                                u'description': u'',
                                u'@id':
                                  u'http://localhost:55001/plone/folder/doc1',
                            },
                        ],
                    },
                ],
            },
        )


class TestDXServicesNavigation(NavigationBase, unittest.TestCase):

    layer = CRN_DX_FUNCTIONAL_TESTING


class TestATServicesNavigation(NavigationBase, unittest.TestCase):

    layer = CRN_AT_FUNCTIONAL_TESTING


class TestDropdownmenu(unittest.TestCase):

    layer = CRN_DX_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

        # we have 2 folders created on the layer right away
        self.root_folders_ids = ['folder-0', 'folder-1']

        setRoles(self.portal, TEST_USER_ID, ['Member'])

    def addSubFolders(self):
        # add some subfolders to one of the folders
        rf = getattr(self.portal, 'folder-0')
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        for i in range(2):
            api.content.create(
                type=u'Folder',
                title=u'Folder',
                id='sub-%s' % 1,  # noqa: S001
                container=rf,
            )
        setRoles(self.portal, TEST_USER_ID, ['Member'])

        return rf.absolute_url()

#    def test_no_subfolders_without_content(self):
#        # since we don't have subfolders yet, we should not have dropdowns
#        for tab_url in [getattr(self.portal, folder_id).absolute_url()
#                        for folder_id in self.root_folders_ids]:
#            self.assertEqual(self.viewlet.getTabObject(tab_url), '')
#
#    def test_dropdownmenus_available(self):
#        rf_url = self.addSubFolders()
#        self.assertNotEqual(
#            self.viewlet.getTabObject(rf_url),
#            '',
#            'We don\'t have the sub-folders available in the global navigation'  # noqa
#        )
#
#    def test_subfolders_in_dropdownmenus(self):
#        rf_url = self.addSubFolders()
#        self.viewlet.update()
#        self.assertIn(
#            'href="http://nohost/plone/folder-0/sub-0"',
#            self.viewlet.getTabObject(rf_url),
#            'The sub-folder\'s URL is not available in the global navigation'
#        )
#
#    def test_leaks_in_dropdownmenus(self):
#        rf_url = self.addSubFolders()
#        self.viewlet.update()
#        self.assertNotIn(
#            'href="http://nohost/plone/folder-0"',
#            self.viewlet.getTabObject(rf_url),
#            'We have the leakage of the top level folders in the dropdownmenus'  # noqa
#        )
