"""Django forms for resume screening."""

from django import forms


class ScreeningForm(forms.Form):
    """Form for uploading resume and job description."""

    RESUME_FILE_TYPES = [
        ('pdf', 'PDF'),
        ('docx', 'Word Document'),
        ('txt', 'Text File'),
    ]

    resume = forms.FileField(
        label='Upload Resume',
        help_text='Supported formats: PDF, DOCX, TXT',
        widget=forms.ClearableFileInput(attrs={
            'class': 'block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-indigo-50 file:text-indigo-700 hover:file:bg-indigo-100',
            'accept': '.pdf,.docx,.txt',
        })
    )

    job_description = forms.CharField(
        label='Job Description',
        help_text='Paste the job description text here',
        widget=forms.Textarea(attrs={
            'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm',
            'rows': 10,
            'placeholder': 'Paste the job description...',
        })
    )