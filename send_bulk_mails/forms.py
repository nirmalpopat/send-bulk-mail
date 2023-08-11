import pandas as pd

from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator

class EmailForm(forms.Form):
    subject = forms.CharField(label='Subject', max_length=144)
    message = forms.CharField(label='Message', widget=forms.Textarea)
    name_column_name = forms.CharField(max_length=144)
    email_column_name = forms.CharField(max_length=144)
    file = forms.FileField(label='File', validators=[FileExtensionValidator(allowed_extensions=['csv', 'xls', 'xlsx'])])

    def clean_file(self):
        uploaded_file = self.cleaned_data.get('file')
        
        if uploaded_file:
            if uploaded_file.name.endswith('.csv'):
                columns_to_read = [self.cleaned_data['name_column_name'], self.cleaned_data['email_column_name']]
                try:
                    data = pd.read_csv(uploaded_file, usecols=columns_to_read)
                except pd.errors.EmptyDataError:
                    raise ValidationError('The CSV file is empty.')
                except ValueError as e:
                    raise ValidationError(str(e))
                except Exception as e:
                    raise ValidationError(str(e))
                
            elif uploaded_file.name.endswith('.xls') or uploaded_file.name.endswith('.xlsx'):
                columns_to_read = [self.cleaned_data['name_column_name'], self.cleaned_data['email_column_name']]
                try:
                    data = pd.read_excel(uploaded_file, usecols=columns_to_read)
                except pd.errors.EmptyDataError:
                    raise ValidationError('The Excel file is empty.')
                except ValueError as e:
                    raise ValidationError(str(e))
                except Exception as e:
                    raise ValidationError(str(e))
                
            else:
                raise ValidationError('Unsupported file format.')

            if not all(col in data.columns for col in columns_to_read):
                raise ValidationError('Required columns not found in the file.')

        return data

