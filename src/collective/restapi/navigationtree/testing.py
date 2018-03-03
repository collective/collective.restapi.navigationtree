# -*- coding: utf-8 -*-
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import collective.restapi.navigationtree


class CollectiveRestapiNavigationtreeLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.app.dexterity
        self.loadZCML(package=plone.app.dexterity)
        self.loadZCML(package=collective.restapi.navigationtree)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'collective.restapi.navigationtree:default')


COLLECTIVE_RESTAPI_NAVIGATIONTREE_FIXTURE = CollectiveRestapiNavigationtreeLayer()


COLLECTIVE_RESTAPI_NAVIGATIONTREE_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_RESTAPI_NAVIGATIONTREE_FIXTURE,),
    name='CollectiveRestapiNavigationtreeLayer:IntegrationTesting'
)


COLLECTIVE_RESTAPI_NAVIGATIONTREE_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_RESTAPI_NAVIGATIONTREE_FIXTURE,),
    name='CollectiveRestapiNavigationtreeLayer:FunctionalTesting'
)


COLLECTIVE_RESTAPI_NAVIGATIONTREE_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        COLLECTIVE_RESTAPI_NAVIGATIONTREE_FIXTURE,
        z2.ZSERVER_FIXTURE
    ),
    name='CollectiveRestapiNavigationtreeLayer:AcceptanceTesting'
)
