from django import forms


class CartAddForm(forms.Form):
    quantity = forms.IntegerField(
        initial=1,
        min_value=1,
        widget=forms.NumberInput(attrs={  
            'step': 1, 
            'type': 'number',
            'class': 'form-control'
        })
    )
    
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
    
    def __init__(self, *args, **kwargs):
        # Extract the stock value and remove it from kwargs
        stock = kwargs.pop('stock', None)
        super().__init__(*args, **kwargs)
        if stock is not None:
            # Set max_value to stock
            self.fields['quantity'].max_value = stock
                                     
    
    