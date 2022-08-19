from django.shortcuts import render
from django.views.generic import TemplateView
from melastic.models import MendeleyGroup, Document
from melastic.forms import AddGroupForm
import melastic.utils as utils
from django.shortcuts import redirect
#FIXME
import melastic.mendeley_driver as md

# Create your views here.

class HomeView(TemplateView):
    """"Just a template view for the landing page."""
    template_name = 'index.html'

#TODO don't prompt internal server errors in the HTML
def admin_add_group(request):
    """Implementation of a controller that will allow the user to add his/her groups and its documents
    to the database."""
    if request.user.is_staff and request.user.is_staff:
        context = {}
        context['form_prueba'] = AddGroupForm(auto_id='user_data2')
        if request.method == 'POST':
            #the condition modification is related to the way the view was coded, trying to use form to keep the password encrypted
            if request.POST['form_id'] == 'user_data':
                mendeley_user = request.POST['mendeley_username']
                mendeley_password = request.POST['mendeley_password']

                # Scan mendeley groups using api.
                try:
                    # login mendeley
                    md.authenticate(mendeley_user, mendeley_password)
                    groups  = md.get_groups()
                    context['groups'] = groups
                    context['mendeley_user'] = mendeley_user
                    context['mendeley_password'] = utils.fernet.encrypt(mendeley_password.encode('utf-8'))
                except Exception as exc:
                    #FIXME change the way we storage this, is better to prompt this in console and promt to the final user
                    # internal server error
                    context['errors'] = [str(exc)]

            elif request.POST['form_id'] == 'groups_data':
                mendeley_user = request.POST['mendeley_user']
                mendeley_password = request.POST['mendeley_password']

                for id, name in request.POST.items():
                    if id == 'form_id' or id == 'csrfmiddlewaretoken' or id == 'mendeley_user' or id == 'mendeley_password':
                        continue
                    # get the group using the ID
                    md.get_group(id)
                    # check if the group exist in the DB
                    try:
                        existing_group = MendeleyGroup.objects.get(mendeley_id=id)
                        # update in the database
                        existing_group.name = name
                        existing_group.mendeley_username = mendeley_user
                        existing_group.mendeley_password = utils.fernet.encrypt(mendeley_password.encode('utf-8'))
                        existing_group.save()
                    except MendeleyGroup.DoesNotExist :
                        # Then create the new object
                        g = MendeleyGroup(
                            mendeley_id=id,
                            name=name,
                            mendeley_username=mendeley_user,
                            mendeley_password=mendeley_password)
                        g.save()

                # redirect to groups view.
                return redirect(to='admin_groups')

        return render(request, 'admin_add_group.html', context)

    else:
        context = {}
        return render(request, 'admin_add_group.html', context)
