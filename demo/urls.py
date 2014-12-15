# Copyright (c) 2011,  2012 Free Software Foundation

#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU Affero General Public License as
#     published by the Free Software Foundation, either version 3 of the
#     License, or (at your option) any later version.

#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU Affero General Public License for more details.

#     You should have received a copy of the GNU Affero General Public License
#     along with this program.  If not, see <http://www.gnu.org/licenses/>.



"""Urls for the demo of Gstudio"""
from django.conf import settings
from django.contrib import admin
from django.conf.urls.defaults import url
from django.conf.urls.defaults import include
from django.conf.urls.defaults import patterns
from django.views.generic.simple import direct_to_template
from django.contrib.auth.views import password_change,password_change_done,login, password_reset_confirm, password_reset, password_reset_done	
from django.contrib.admin.sites import AdminSite
from django.contrib.auth.decorators import login_required

from gstudio.sitemaps import TagSitemap
from gstudio.sitemaps import NodetypeSitemap
from gstudio.sitemaps import MetatypeSitemap
from gstudio.sitemaps import AuthorSitemap
from gstudio.forms import *
from objectapp.sitemaps import GbobjectSitemap

from registration.views import register
from views import home_view, more_view, nroer_view, proceed_view
from decorator import decorated_includes


admin.autodiscover()
handler500 = 'demo.views.server_error'
handler404 = 'django.views.defaults.page_not_found'

urlpatterns = patterns(
    '',
    (r'^$', 'django.views.generic.simple.redirect_to',
     {'url': '/home/'}),
    url(r'^home/', nroer_view),
    url(r'^nroer/', home_view),
    #url(r'^browserError', browserError_view),
    url(r'^proceed', proceed_view),
    url(r'^browserError/', direct_to_template, {'template': 'gstudio/browserError.html'}),
   # url(r'^more/',more_view),
    url(r'^gstudio/', include('gstudio.urls')),
    url(r'^nodetypes/', include('gstudio.urls')),
    url(r'^objects/', include('objectapp.urls')),
    #url(r'^tagclouds/',include('gstudio.urls.tagclouds')),
    url(r'^comments/', include('django.contrib.comments.urls')),
    url(r'^browsecollection/','gstudio.views.browseCollection.browseCollection'),
    url(r'^collection/(\w+)/','gstudio.views.collection.collection'),
    url(r'^AboutUs/', direct_to_template, {'template': 'gstudio/aboutUs.html'}),
    url(r'^TermsOfUse/', direct_to_template, {'template': 'gstudio/termsOfUse.html'}),
    url(r'^EnrichTimeline/', direct_to_template, {'template': 'gstudio/enrichtimeline.html'}),
    url(r'^ShareResources/', direct_to_template, {'template': 'gstudio/shareresources.html'}),
    url(r'^KnowledgeKingdom/', direct_to_template, {'template': 'gstudio/knowledgekingdom.html'}),
    url(r'^RejuvenatingHistory/', direct_to_template, {'template': 'gstudio/rejuvenatinghistory.html'}),
    url(r'^CaptureNature/', direct_to_template, {'template': 'gstudio/capturenature.html'}),
    url(r'^ScienceinHands/', direct_to_template, {'template': 'gstudio/scienceinhands.html'}),
    url(r'^SharingIdeas/', direct_to_template, {'template': 'gstudio/sharingideas.html'}),
    url(r'^VoicetoMasses/', direct_to_template, {'template': 'gstudio/voicetomasses.html'}),
    url(r'^ShareKnowledge/', direct_to_template, {'template': 'gstudio/shareknowledge.html'}),
    url(r'^CommentOnResources/', direct_to_template, {'template': 'gstudio/commentonresources.html'}),
    url(r'^ContactUs/', direct_to_template, {'template': 'gstudio/contactUs.html'}),
    url(r'^Contribute/', direct_to_template, {'template': 'gstudio/contribute.html'}),
    url(r'^SrinivasaRamanujan/', direct_to_template, {'template': 'gstudio/ramanujan.html'}),
    url(r'^EnrichTheTimeline/', direct_to_template, {'template': 'gstudio/enrichthetimeline.html'}),
    url(r'^MagicSquare/', direct_to_template, {'template': 'gstudio/magicsquare.html'}),
    url(r'^MathsTricks/', direct_to_template, {'template': 'gstudio/mathstricks.html'}),
    url(r'^ILoveMaths/', direct_to_template, {'template': 'gstudio/ilovemaths.html'}),
    url(r'^ConstitutionCalling/', direct_to_template, {'template': 'gstudio/constitution.html'}),
    url(r'^ConstitutionShareResources/', direct_to_template, {'template': 'gstudio/constitutionshareresources.html'}),
    url(r'^ConstitutionEnrichTimeline/', direct_to_template, {'template': 'gstudio/constitutionenrichtimeline.html'}),
    url(r'^ConstitutionShareKnowledge/', direct_to_template, {'template': 'gstudio/constitutionshareknowledge.html'}),
    url(r'^MyHand/', direct_to_template, {'template': 'gstudio/myhand.html'}),
    url(r'^Democratic/', direct_to_template, {'template': 'gstudio/democratic.html'}),
    url(r'^Amendment/', direct_to_template, {'template': 'gstudio/amendment.html'}),
    url(r'^CourseOnOERFindOutMore/', direct_to_template, {'template': 'gstudio/eventpage2.html'}),
    url(r'^CourseOnOER/', direct_to_template, {'template': 'gstudio/eventpage.html'}),
    url(r'^DiscoverPatterns/', direct_to_template, {'template': 'gstudio/discoverpatterns.html'}),
    url(r'^NaturePatterns/', direct_to_template, {'template': 'gstudio/naturepatterns.html'}),
    url(r'^ArtPatterns/', direct_to_template, {'template': 'gstudio/artpatterns.html'}),
    url(r'^Tangram/', direct_to_template, {'template': 'gstudio/tangram.html'}),
    url(r'^TurtleArt/', direct_to_template, {'template': 'gstudio/turtlepatterns.html'}),
    url(r'^ShareCreativity/', direct_to_template, {'template': 'gstudio/sharecreativity.html'}),
    
    url(r'^contribute/resources', direct_to_template, {'template': 'gstudio/contrib_resource.html'}),
    url(r'^ShareResources/', direct_to_template, {'template': 'gstudio/shareresources.html'}),
    url(r'^ContributeResourceForm/', direct_to_template, {'template': 'gstudio/contributeresform.html'}),
    url(r'^ContributeForm2/', direct_to_template, {'template': 'gstudio/contributeresform2.html'}),
    url(r'^dashboard/','gstudio.views.dashboard.dashboard'),
    url(r'^translate/',include('gstudio.urls.translate')),
    url(r'^contribute/theresources', direct_to_template, {'template': 'gstudio/contribute_resource.html'}),
url(r'^Ganit/', direct_to_template, {'template': 'gstudio/GanitPoster.html'}),
url(r'^FunWithGeogebra/', direct_to_template, {'template': 'gstudio/FunWithGeogebra.html'}),
url(r'^ExploringMathKits/', direct_to_template, {'template': 'gstudio/ExploringMathKits.html'}),
url(r'^GanitMagicSquare/', direct_to_template, {'template': 'gstudio/GanitMagicSquare.html'}),
url(r'^KnowSrinivasa/', direct_to_template, {'template': 'gstudio/KnowSrinivasa.html'}),
url(r'^MoreonMaths/', direct_to_template, {'template': 'gstudio/MoreonMaths.html'}),
url(r'^GanitInnerTemplate/', direct_to_template, {'template': 'gstudio/GanitInnerTemplate.html'}),
    #URL for XMLRPC
    #url(r'^xmlrpc/$','django_xmlrpc.views.handle_xmlrpc'),
    #url(r'^i18n/', include('django.conf.urls.i18n')),
    #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/gstudio/', include('gstudio.urls.ajaxurls')),
    url(r'^admin/password_change/', password_change,{'password_change_form':UserChangeform,'template_name':'registration/password_change_form1.html'}),
    url(r'^account/password/change/', password_change,{'password_change_form':UserChangeform,'template_name':'registration/password_change_form1.html'}),
    url(r'^accounts/password/change/done/', password_change_done,{'template_name':'registration/password_change_done1.html'}),
    url(r'^admin/', decorated_includes(login_required,include(admin.site.urls))),
    url(r'^objects/admin/', decorated_includes(login_required,include(admin.site.urls))),
    url(r'^nodetypes/admin/', decorated_includes(login_required,include(admin.site.urls))),
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^notification/',include('notification.urls')),
    url(r'^accounts/register/$', register, {'backend': 'gstudio.regbackend.MyBackend','form_class': UserRegistrationForm}, name='registration_register'),
    url(r'^accounts/login/', login,{'authentication_form':UserLogin}),
    url(r'^accounts/password/reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',password_reset_confirm,{'set_password_form':UserResetform,'template_name':'registration/password_reset_confirm1.html'}),
    url(r'^accounts/password/reset/done/', password_reset_done,{'template_name':'registration/password_reset_done1.html'}),
    url(r'^accounts/password/reset/', password_reset,{'template_name':'registration/password_reset_form1.html'}),
    url(r'^accounts/', include('registration.urls')),

    url(r'^$', 'django.views.generic.simple.redirect_to',
            { 'template': 'index.html' }, 'index'),
    )

sitemaps = {'tags': TagSitemap,
            'blog': NodetypeSitemap,
            'authors': AuthorSitemap,
            'objecttypes': MetatypeSitemap,
            'gbobjects': NodetypeSitemap}

urlpatterns += patterns(
    'django.contrib.sitemaps.views',
    url(r'^sitemap.xml$', 'index',
        {'sitemaps': sitemaps}),
    url(r'^sitemap-(?P<section>.+)\.xml$', 'sitemap',
        {'sitemaps': sitemaps}),
    )

urlpatterns += patterns(
    '',
    url(r'^404/$', 'django.views.defaults.page_not_found'),
    url(r'^500/$', 'demo.views.server_error'),
    )

if settings.DEBUG:
    urlpatterns += patterns(
        '',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT})
        )
