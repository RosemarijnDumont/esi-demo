from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from ..models import TrialAccount, SSOConfiguration
from ..forms import SSOConfigurationForm

@login_required
def configure_trial_sso(request, account_id):
    trial_account = TrialAccount.objects.get(id=account_id)
    try:
        sso_config = SSOConfiguration.objects.get(account=trial_account)
    except SSOConfiguration.DoesNotExist:
        sso_config = SSOConfiguration(account=trial_account)

    if request.method == 'POST':
        form = SSOConfigurationForm(request.POST, instance=sso_config)
        if form.is_valid():
            form.save()
            # Log the action for auditing
            return redirect('trial_account_detail', account_id=account_id)
    else:
        form = SSOConfigurationForm(instance=sso_config)

    return render(request, 'admin/configure_sso.html', {'form': form, 'account': trial_account})