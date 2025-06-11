from django import forms
from .models import User, Listing, Bids, Category

class AddListingForm(forms.Form):
    category = forms.ModelChoiceField(label="Category: ", queryset=Category.objects.all(), to_field_name="name")
    title = forms.CharField(initial="Title", label="Title: ", max_length="100", 
                            help_text='100 characters max.',
                            error_messages={'required': 'Please enter a Title'})

    description = forms.CharField(initial="A good item", label="Small item description: ", max_length="800",
                                 help_text='800 characters max.',
                                 error_messages={'required': 'Please enter a description of the item'})
    
    start_bid = forms.DecimalField(initial=00.00, label="Starting Bid: ", decimal_places=2, max_digits=10,
                                   error_messages={'required': 'Please enter a starting bid value'})
    
    image_url = forms.URLField(initial="https://static.vecteezy.com/system/resources/previews/010/279/249/non_2x/carton-box-color-icon-illustration-vector.jpg", label="Image Url: ", required=False)


class AddCommentForm(forms.Form):
    comment = forms.CharField(max_length="600",
                              error_messages={
                              'required': 'Please enter a starting bid value'
                              })


