from django import forms

class FormContacto(forms.Form):
    nombre = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Juan'})
    )
    apellido = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Pérez'})
    )
    telefono = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '1234567890'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'juan@example.com'})
    )
    asunto = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Asunto'})
    )
    mensaje = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Tu mensaje aquí', 'rows': 4})
    )
    
class FormComentario(forms.Form):
    nombre_completo = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Juan'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'juan@example.com'})
    )
    comentario = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Tu comentario aqui', 'rows': 4})
    )    

    