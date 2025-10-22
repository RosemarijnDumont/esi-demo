from django.db import models

class TrialAccount(models.Model):
    name = models.CharField(max_length=255)
    # Other trial account fields
    def __str__(self):
        return self.name

class SSOConfiguration(models.Model):
    account = models.OneToOneField(TrialAccount, on_delete=models.CASCADE)
    sso_enabled = models.BooleanField(default=False)
    idp_metadata_url = models.URLField(blank=True, null=True)
    entity_id = models.CharField(max_length=255, blank=True, null=True)
    acs_url = models.URLField(blank=True, null=True)
    x509cert = models.TextField(blank=True, null=True)
    # Add other SAML specific fields as needed

    def __str__(self):
        return f"SSO Config for {self.account.name}"