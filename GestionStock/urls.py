"""
URL configuration for GestionStock project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Stock import views_typeequipement
from Stock import views_produit
from Stock import views_client
from Stock import views_partnumber
from Stock import views_dashboard
from Stock import views_pays

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views_dashboard.dashboard, name='dashboard'),
    path('mouvpartnumber/', views_dashboard.mouv_partnumber_data, name='mouvpartnumber'),
    
    path('typeequipement/', views_typeequipement.typeequipement, name='typeequipement'),
    path('savetypeequipement/', views_typeequipement.savetypeequipement, name='savetypeequipement'),
    path('deleteTypeEquipement/', views_typeequipement.deleteTypeEquipement, name='deleteTypeEquipement'),
    
    path('listepays/', views_pays.pays, name='listepays'),
    path('enregistrepays/', views_pays.savepays, name='enregistrepays'),
    path('deletepays/', views_pays.deletepays, name='deletepays'),

    path('client/', views_client.ListClient, name='client'),
    path('enregistreclient/', views_client.saveclient, name='enregistreclient'),
    path('delete_client/', views_client.deleteClient, name='delete_client'),
    
    path('partnumber/', views_partnumber.ListPartNumber, name='partnumber'),
    path('enregistrepartnumber/', views_partnumber.savepartnumber, name='enregistrepartnumber'),
    path('delete_partnumber/', views_partnumber.deletepartnumber, name='delete_partnumber'),

    path('stock/', views_produit.inserer_produit, name='stock'),
    path('export-data/', views_produit.export_all_data, name='export_all_data'),
    path('get-produit/<str:serial_number>/', views_produit.get_produit_data, name='get_produit'),
    path('mis_qte/', views_produit.mis_qte, name='mis_qte'),
    path('Insertion_Prdt/', views_produit.InsertionPrdt, name='mis_qte'),
    path('detail_materiel/', views_produit.mouv_produit_data, name='detail_prdt'),
    path('export-data-mouv/', views_produit.export_all_data_mouv, name='export_all_data_mouv'),
]
