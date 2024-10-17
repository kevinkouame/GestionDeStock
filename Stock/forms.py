from django import forms
from django.db import connection

class ProduitForm(forms.Form):
    part_number = forms.CharField(max_length=250, label="Part Number", widget=forms.TextInput(attrs={'id': 'PART_NUMBER'}), required=True)
    designation = forms.CharField(max_length=250, label="Designation", widget=forms.TextInput(attrs={'id': 'DESIGNATION'}))
    serial_number = forms.CharField(max_length=250, label="Serial Number", widget=forms.TextInput(attrs={'id': 'SERIAL_NUMBER'}))
    type_equipement = forms.CharField(max_length=250, label="Type Equipement", widget=forms.TextInput(attrs={'id': 'TYPE_EQUIPEMENT'}))
    seuil_alerte = forms.IntegerField(label="Seuil d'alerte", min_value=0, widget=forms.NumberInput(attrs={'id': 'SEUIL_ALERTE'}))
    #id_emplacement = forms.IntegerField(label="ID Emplacement")
    # Liste déroulante pour les emplacements
    id_emplacement = forms.ChoiceField(choices=[], label="Emplacement", widget=forms.Select(attrs={'id': 'ID_EMPLACEMENT'}))  # Les choix seront remplis dans la vue
    detail_emplacement = forms.CharField(label="Detail Emplacement", widget=forms.Textarea(attrs={'id': 'DETAIL_EMPLACEMENT'}))
    Quantite_Stock = forms.IntegerField(label="Quantité en Stock", initial=0, widget=forms.NumberInput(attrs={'id': 'FORM_QUANTITE_STOCK'}) )


    Operation = forms.ChoiceField(choices=[], label="Opération", widget=forms.Select(attrs={'id': 'ID_OPERATION'}))
    Quantite = forms.IntegerField(label="Quantité", initial=0, widget=forms.NumberInput(attrs={'id': 'QUANTITE'}) )
    commentaire_qte = forms.CharField(label="Commentaire", initial="vide", widget=forms.Textarea(attrs={'id': 'COMMENTAIRE'}))
    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Charger dynamiquement les choix d'emplacement depuis la base de données
        self.fields['id_emplacement'].choices = self.get_emplacement_choices()
        self.fields['Operation'].choices = self.get_type_mouvement()
        

    def get_emplacement_choices(self):
        # Récupérer les données pour le tableau à partir de la procédure stockée LISTE_PRODUIT
        with connection.cursor() as cursor:
            cursor.execute("{CALL [dbo].[LISTE_EMPLACEMENT]}")
            emplacements = cursor.fetchall()  # Récupère les résultats sous forme de liste de tuples

        emplacement_choices = [(emp[0], f"{emp[1]} ({emp[3]})") for emp in emplacements]

        return emplacement_choices   



    def get_type_mouvement(self):
        # Récupérer les données pour le tableau à partir de la procédure stockée LISTE_PRODUIT
        with connection.cursor() as cursor:
            cursor.execute("{CALL [dbo].[LISTE_TYPE_MOUVEMENT]}")
            type_mouvement = cursor.fetchall()  # Récupère les résultats sous forme de liste de tuples

        type_mouvement_choices = [(emp[0], emp[1]) for emp in type_mouvement]

        return type_mouvement_choices    