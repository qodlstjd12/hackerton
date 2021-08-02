
def save(self, commit=True):
    user = super(CsRegisterForm, self).save(commit=False)
    user.is_active = False
    user.save()