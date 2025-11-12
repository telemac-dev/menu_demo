# user_management/forms.py
# Formulários para Registro e Perfil de Usuários
from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User, Group, Permission
from .models import UserProfile

class UserRegistrationForm(UserCreationForm):
    """
    Formulário para registro de novos usuários.
    """
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user

class UserProfileForm(forms.ModelForm):
    """
    Formulário para edição do perfil do usuário.
    """
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = UserProfile
        fields = ('bio', 'position', 'department', 'phone', 'profile_image')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email

    def save(self, commit=True):
        profile = super().save(commit=False)
        profile.user.first_name = self.cleaned_data['first_name']
        profile.user.last_name = self.cleaned_data['last_name']
        profile.user.email = self.cleaned_data['email']

        if commit:
            profile.user.save()
            profile.save()

        return profile

class UserPermissionForm(forms.Form):
    """
    Formulário para gerenciamento de permissões de usuários.
    """
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if self.user:
            self.fields['groups'].initial = self.user.groups.all()

            # Agrupa permissões por app e modelo
            permissions = Permission.objects.all().select_related('content_type')
            permission_dict = {}

            for perm in permissions:
                app_label = perm.content_type.app_label
                model = perm.content_type.model

                if app_label not in permission_dict:
                    permission_dict[app_label] = {}

                if model not in permission_dict[app_label]:
                    permission_dict[app_label][model] = []

                permission_dict[app_label][model].append(perm)

            # Cria campos para cada grupo de permissões
            for app_label in sorted(permission_dict.keys()):
                for model in sorted(permission_dict[app_label].keys()):
                    field_name = f"permissions_{app_label}_{model}"
                    model_perms = permission_dict[app_label][model]

                    self.fields[field_name] = forms.ModelMultipleChoiceField(
                        queryset=Permission.objects.filter(id__in=[p.id for p in model_perms]),
                        required=False,
                        widget=forms.CheckboxSelectMultiple,
                        label=f"{app_label.title()} - {model.title()}"
                    )

                    # Define valores iniciais
                    if self.user:
                        self.fields[field_name].initial = self.user.user_permissions.filter(
                            content_type__app_label=app_label,
                            content_type__model=model
                        )

    def save(self):
        if not self.user:
            return

        # Atualiza grupos
        self.user.groups.set(self.cleaned_data['groups'])

        # Limpa todas as permissões diretas
        self.user.user_permissions.clear()

        # Adiciona permissões selecionadas
        for field_name, value in self.cleaned_data.items():
            if field_name.startswith('permissions_') and value:
                self.user.user_permissions.add(*value)
