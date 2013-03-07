from django.views.generic import FormView, TemplateView
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from dotcloud.client import RESTClient
from dotcloud.client.errors import RESTAPIError
from dotcloud.client.auth import BasicAuth
from kicker.models import Kick

class KickerView (TemplateView):
    template_name = 'kicker/kicker.html'

    def get_dotcloud_user(self):
        apikey = settings.DOTCLOUD['APIKEY']
        appname = settings.DOTCLOUD['APPNAME']

        username, password = apikey.split(':')
        client = RESTClient()
        client.authenticator = BasicAuth(username, password)
        user = client.make_prefix_client('/me'.format(username))
        return user

    def get_application_data(self):
        """
        Query the DotCloud API for data about the application specified in the
        settings.
        """
        appname = settings.DOTCLOUD['APPNAME']
        user = self.get_dotcloud_user()
        app = user.get('/applications/{0}'.format(appname))
        return app.obj

    def kick(self, appname, servname, instid):
        user = self.get_dotcloud_user()
        url = '/applications/{0}/services/{1}/instances/{2}/status' \
            .format(appname, servname, instid)
        try:
            user.put(url, {'status': 'restart'})
        except RESTAPIError as e:
            return None

        machine = self.get_machine_name(appname, servname, instid)
        kick = Kick()
        kick.machine = machine
        kick.kicker = self.request.user
        kick.save()
        return kick

    def get_machine_name(self, appname, servname, instid):
        return '%s.%s.%s' % (appname, servname, instid)

    def get_all_kicks(self):
        """
        Get all the kicks for a particular application. This will help us cut
        down on the number of queries our application has to make.
        """
        if not hasattr(self, '_kicks'):
            appname = settings.DOTCLOUD['APPNAME']
            self._kicks = Kick.objects\
                .filter(machine__startswith=appname)\
                .order_by('-at')
        return self._kicks

    def get_latest_kick(self, servname, instid):
        """
        Get the latest kick for the configured application, given service name,
        and given instance id.
        """
        appname = settings.DOTCLOUD['APPNAME']
        kicks = self.get_all_kicks()
        for kick in kicks:
            if kick.machine == self.get_machine_name(appname, servname, instid):
                return kick
        return None

    def get_context_data(self, **kwargs):
        context = super(KickerView, self).get_context_data(**kwargs)

        application = self.get_application_data()
        for service in application['services']:
            for instance in service['instances']:
                latest_kick = self.get_latest_kick(
                    service['name'], instance['instance_id'])
                instance['latest_kick'] = latest_kick

        context['application'] = application
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(KickerView, self).dispatch(*args, **kwargs)

    def post(self, request):
        application = request.POST.get('application')
        service = request.POST.get('service')
        instance = request.POST.get('instance')
        kick = self.kick(application, service, instance)

        # TODO: If ajax, return 400 when kick is None. Otherwise, use messages
        #       framework.

        return redirect('kicker')


kicker_view = KickerView.as_view()
