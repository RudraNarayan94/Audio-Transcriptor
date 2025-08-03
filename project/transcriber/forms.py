from django import forms

class AudioUploadForm(forms.Form):
    audio_file = forms.FileField(label='Select an audio file (.mp3 or .wav)')
    file_type = forms.ChoiceField(choices=[('txt', 'Text File (.txt)'), ('docx', 'Word Document (.docx)')], initial='txt')