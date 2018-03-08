# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import login
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.testing import z2
from Products.CMFCore.utils import getToolByName

import collective.restapi.navigationtree


class CollectiveRestapiNavigationtreeDXLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.restapi
        import webcouturier.dropdownmenu
        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=webcouturier.dropdownmenu)
        self.loadZCML(package=collective.restapi.navigationtree)
        z2.installProduct(app, 'collective.restapi.navigationtree')

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'collective.restapi.navigationtree:default')
        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)
        workflowTool = getToolByName(portal, 'portal_workflow')   # noqa: P001
        workflowTool.setDefaultChain('simple_publication_workflow')
        for i in range(2):
            folder_id = 'folder-{0}'.format(i)
            portal.invokeFactory('Folder', folder_id)  # noqa: P001
        setRoles(portal, TEST_USER_ID, ['Member'])


CRN_DX_FIXTURE = CollectiveRestapiNavigationtreeDXLayer()


CRN_DX_INTEGRATION_TESTING = IntegrationTesting(
    bases=(CRN_DX_FIXTURE,),
    name='CollectiveRestapiNavigationtreeDXLayer:IntegrationTesting',
)


CRN_DX_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(CRN_DX_FIXTURE, z2.ZSERVER_FIXTURE),
    name='CollectiveRestapiNavigationtreeDXLayer:FunctionalTesting',
)


class CollectiveRestapiNavigationtreeATLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.restapi
        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=collective.restapi.navigationtree)
        z2.installProduct(app, 'collective.restapi.navigationtree')

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'collective.restapi.navigationtree:default')


CRN_AT_FIXTURE = CollectiveRestapiNavigationtreeATLayer()


CRN_AT_INTEGRATION_TESTING = IntegrationTesting(
    bases=(CRN_AT_FIXTURE,),
    name='CollectiveRestapiNavigationtreeATLayer:IntegrationTesting',
)


CRN_AT_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(CRN_AT_FIXTURE, z2.ZSERVER_FIXTURE),
    name='CollectiveRestapiNavigationtreeATLayer:FunctionalTesting',
)
