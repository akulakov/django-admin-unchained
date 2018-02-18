from django.shortcuts import render

from django.views.generic import ListView, TemplateView
from django.contrib.admin.views.main import ChangeList
try:
    from django.core.urlresolvers import reverse_lazy
except ImportError:
    from django.urls import reverse_lazy
from django.contrib.admin import helpers, widgets
from django.shortcuts import render, reverse
from django.contrib.admin import actions


class AUChangeList(ChangeList):
    def url_for_result(self, result):
        return self.model_admin.get_change_url(result, self.pk_attname)

class MockAdminSite:
    name = ''
    empty_value_display = ''
    actions = ()

    def __init__(self, *args, **kwargs):
        self._registry = {}

    def each_context(self, request):
        return {}

    def get_action(self, request):
        return

    def is_registered(self, model):
        return True


class AUAddOrChangeView(TemplateView):
    model = None
    pk_url_kwarg = "object_id"
    fields = []
    success_url = None
    admin_class = None
    delete_url_name = None

    def dispatch(self, request, *args, **kwargs):
        if request.method in ('GET', 'POST'):
            model_admin = self.admin_class(self.model, MockAdminSite())
            model_admin.redirect_url = str(self.success_url)
            pk = self.kwargs.get('pk')
            delete_url = reverse(self.delete_url_name, kwargs=dict(pk=pk))
            extra_context = dict(show_history=model_admin.show_history, delete_url=delete_url)
            if pk:
                return model_admin.change_view(request, pk, extra_context=extra_context)
            else:
                return model_admin.add_view(request, extra_context=extra_context)

class AUDeleteView(TemplateView):
    model = None
    pk_url_kwarg = "object_id"
    fields = []
    success_url = None
    admin_class = None

    def dispatch(self, request, *args, **kwargs):
        if request.method in ('GET', 'POST'):
            model_admin = self.admin_class(self.model, MockAdminSite())
            model_admin.redirect_url = str(self.success_url)
            pk = self.kwargs.get('pk')
            return model_admin.delete_view(request, pk)


class AUListView(ListView):
    model = None
    pk_url_kwarg = "object_id"
    fields = []
    admin_class = None
    template_name = 'admin_unchained/change_list.html'

    def get_context_data(self, **kwargs):
        context = super(AUListView, self).get_context_data(**kwargs)

        model_admin = self.admin_class(self.model, MockAdminSite())
        opts = model_admin.model._meta
        request = self.request

        list_display = model_admin.get_list_display(request)
        list_display_links = model_admin.get_list_display_links(request, list_display)
        list_filter = model_admin.get_list_filter(request)
        search_fields = model_admin.get_search_fields(request)
        list_select_related = model_admin.get_list_select_related(request)

        actions = model_admin.get_actions(request)
        media = model_admin.media
        if actions:
            action_form = model_admin.action_form(auto_id=None)
            action_form.fields['action'].choices = model_admin.get_action_choices(request)
            media += action_form.media
        else:
            action_form = None

        if actions:
            list_display = ['action_checkbox'] + list(list_display)

        cl = AUChangeList(
            request, model_admin.model, list_display,
            list_display_links, list_filter, model_admin.date_hierarchy,
            search_fields, list_select_related, model_admin.list_per_page,
            model_admin.list_max_show_all, model_admin.list_editable, model_admin,
        )

        self.model_admin = model_admin
        self.actions = actions

        cl.formset=None
        context.update({
            'opts': opts,
            'cl': cl,
            'action_form': action_form,
            'add_url': model_admin.get_add_url(request),
            'actions_on_top': model_admin.actions_on_top,
            'actions_on_bottom': model_admin.actions_on_bottom,
            'has_add_permission': model_admin.has_add_permission(request),
        })

        return context

    def post(self, request, *args, **kwargs):
        self.object_list = self.model.objects.all()
        data = self.get_context_data()
        action_failed = False
        cl = data.get('cl')
        selected = request.POST.getlist(helpers.ACTION_CHECKBOX_NAME)

        # Actions with no confirmation
        if (self.actions and 'index' in request.POST and '_save' not in request.POST):
            if selected:
                response = self.model_admin.response_action(request, queryset=cl.get_queryset(request))
                if response:
                    return response
                else:
                    action_failed = True
            else:
                msg = _("Items must be selected in order to perform "
                        "actions on them. No items have been changed.")
                self.model_admin.message_user(request, msg, messages.WARNING)
                action_failed = True

        # Actions with confirmation
        if (self.actions and helpers.ACTION_CHECKBOX_NAME in request.POST and
                'index' not in request.POST and '_save' not in request.POST):
            if selected:
                response = self.model_admin.response_action(request, queryset=cl.get_queryset(request))
                if response:
                    return response
                else:
                    action_failed = True

        if action_failed:
            # Redirect back to the changelist page to avoid resubmitting the
            # form if the user refreshes the browser or uses the "No, take
            # me back" button on the action confirmation page.
            return HttpResponseRedirect(request.get_full_path())

