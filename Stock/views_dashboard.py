import pandas as pd
import time
from django.shortcuts import render
from django.http import HttpResponse

from django.shortcuts import render, redirect
from django.db import connection
from .forms import ProduitForm
from django.contrib import messages
from django.http import JsonResponse
from io import BytesIO


import json
#from django.shortcuts import get_object_or_404
#from .models import Produit  # Ton modèle de produit


def dashboard(request):


    # Récupérer les données pour le tableau à partir de la procédure stockée LISTE_PRODUIT
    with connection.cursor() as cursor:
        cursor.execute("{cALL [dbo].[LISTE_DASHBOARD]}")
        produits_data = cursor.fetchall()  # Récupère les résultats sous forme de liste de tuples
        print(produits_data)  # Imprime les données récupérées pour vérifier leur structure

    if request.method == 'POST':
        form = ProduitForm(request.POST)  # Utilise le formulaire ProduitForm avec les données POST
        if form.is_valid():
            # Récupérer les données du formulaire
            part_number = form.cleaned_data['part_number']
            designation = str(form.cleaned_data['designation'])
            serial_number = str(form.cleaned_data['serial_number'])
            type_equipement = str(form.cleaned_data['type_equipement'])
            id_emplacement = int(form.cleaned_data['id_emplacement'])
            seuil_alerte = int(form.cleaned_data['seuil_alerte'])
            detail_emplacement = str(form.cleaned_data['detail_emplacement'])
            sender = 0

            if(int(seuil_alerte) > 0):

                #with connection.cursor() as cursor:
                #    cursor.execute("{cALL [dbo].[PS_PRODUIT] (""'"+ part_number +"'"",""'"+designation+"'"",""'"+serial_number+"'"",""'"+type_equipement+"'"",""'"+str(id_emplacement)+"'"",""'"+str(seuil_alerte)+"'"",""'"+detail_emplacement+"'"",0)}")
                #    result = cursor.fetchone()  # ou cursor.fetchone() selon le cas

                with connection.cursor() as cursor:
                    cursor.execute(
                        "{cALL [dbo].[PS_PRODUIT] (%s, %s, %s, %s, %s, %s, %s, 0)}",
                        [
                            part_number,
                            designation,
                            serial_number,
                            type_equipement,
                            str(id_emplacement),
                            str(seuil_alerte),
                            detail_emplacement,
                        ]
                    )
                    result = cursor.fetchone()  # ou cursor.fetchall() selon le cas
            
                # Récupérer le retour de la procédure, par exemple, un message ou un code d'erreur
                if result:
                    code_retour = result[0]
                    if code_retour == part_number:  # Enregistrement avec succès
                        messages.success(request, 'Matériel inséré avec succès.')
                    else:  # part_number existe déjà
                        messages.error(request, 'Erreur : le numéro de pièce existe déjà.')
            else:
                messages.error(request, 'Erreur : Le seuil ne peut pas être supérieur à 0.')

            return redirect('inserer_produit')

    else:
        form = ProduitForm()  # Crée une instance vide du formulaire pour l'affichage initial
        #form.fields['id_emplacement'].choices = emplacement_choices

    #return render(request, 'inserer_produit.html', {'form': form})  # Envoie le formulaire au template
    return render(request, 'stock/dashboard.html', {'form': form, 'produits_data': produits_data})




def InsererProduitAjax(request):
    if request.method == 'POST':
        form = ProduitForm(request.POST)  # Utilise le formulaire ProduitForm avec les données POST
        if form.is_valid():
            # Récupérer les données du formulaire
            part_number = form.cleaned_data['part_number']
            designation = form.cleaned_data['designation']
            serial_number = form.cleaned_data['serial_number']
            type_equipement = form.cleaned_data['type_equipement']
            id_emplacement = form.cleaned_data['id_emplacement']
            detail_emplacement = form.cleaned_data['detail_emplacement']
            sender = form.cleaned_data['sender']
            
            # Appeler la procédure stockée
            with connection.cursor() as cursor:
                cursor.callproc('[dbo].[PS_PRODUIT]', [
                    part_number,
                    designation,
                    serial_number,
                    type_equipement,
                    id_emplacement,
                    detail_emplacement,
                    sender
                ])

                # Récupérer le retour de la procédure, par exemple, un message ou un code d'erreur
                result = cursor.fetchone()  # ou cursor.fetchall() selon le cas
            
            if result and result[0] == 0:  # Enregistrement avec succès
                return JsonResponse({'success': True, 'message': 'Matériel inséré avec succès.'})
            else:  # part_number existe déjà
                return JsonResponse({'success': False, 'message': 'Le numéro de pièce existe déjà.'})
            return JsonResponse({'success': True, 'message': 'Matériel inséré avec succès.'})
        else:
            return JsonResponse({'success': False, 'message': 'Données invalides.'})

    #else:
    form = ProduitForm()  # Crée une instance vide du formulaire pour l'affichage initial

    return render(request, 'InsererProduitAjax.html', {'form': form})  # Envoie le formulaire au template



def export_all_data(request):
    # Appel de la procédure stockée LISTE_PRODUIT
    with connection.cursor() as cursor:
        #cursor.execute("EXEC [dbo].[LISTE_PRODUIT_TELECHARGEMENT]")  # Exécute la procédure stockée
        cursor.execute("{cALL [dbo].[LISTE_PRODUIT] (0)}")
        rows = cursor.fetchall()

        # Récupérer les colonnes à partir du curseur
        columns = [col[0] for col in cursor.description]

    # Utilisation de pandas pour convertir les données en DataFrame
    df = pd.DataFrame.from_records(rows, columns=columns)

    # Créer un fichier Excel en mémoire
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Liste Produits')
    writer.close()  # Remplacer save() par close()
    output.seek(0)

    # Préparer la réponse HTTP pour le téléchargement
    response = HttpResponse(output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=materiels_complets.xlsx'

    return response



def export_all_data_mouv(request):
    if request.method == 'GET':
        # Récupérez le paramètre 'label_content'
        part_number = request.GET.get('label_content', None)

        # Appel de la procédure stockée LISTE_PRODUIT
        #with connection.cursor() as cursor:
        #    cursor.execute("{cALL [dbo].[MOUV_PRODUIT] (""'"+ part_number +"'"")}")
        #    rows = cursor.fetchall()

        with connection.cursor() as cursor:
            cursor.execute(
                "{CALL [dbo].[MOUV_PRODUIT] (%s)}",
                [part_number]
            )
            # Récupérer tous les enregistrements
            rows = cursor.fetchall()

            # Récupérer les colonnes à partir du curseur
            columns = [col[0] for col in cursor.description]

        # Utilisation de pandas pour convertir les données en DataFrame
        df = pd.DataFrame.from_records(rows, columns=columns)

        # Créer un fichier Excel en mémoire
        output = BytesIO()
        writer = pd.ExcelWriter(output, engine='xlsxwriter')
        df.to_excel(writer, index=False, sheet_name='Liste Produits')
        writer.close()  # Remplacer save() par close()
        output.seek(0)

        # Préparer la réponse HTTP pour le téléchargement
        response = HttpResponse(output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename='+part_number+'.xlsx'

        return response



def get_produit_data(request, serial_number):
    # Rechercher le produit avec le part_number donné
    #with connection.cursor() as cursor:
    #    cursor.execute("{cALL [dbo].[INFO_PRODUIT] (""'"+ part_number +"'"")}")              
    #    result = cursor.fetchone()  # Récupérer un enregistrement

    with connection.cursor() as cursor:
        # Appel de la procédure stockée avec des paramètres
        cursor.execute("{cALL [dbo].[INFO_PRODUIT] (%s)}", [serial_number])
        result = cursor.fetchone()  # Récupérer un enregistrement

        # Si aucun résultat n'est trouvé, renvoyer un message d'erreur
        if result is None:
            return JsonResponse({"error": "Matériel non trouvé"}, status=404)

        # Obtenir les noms des colonnes à partir de cursor.description
        columns = [desc[0] for desc in cursor.description]

    # Convertir le tuple en dictionnaire
    result_dict = dict(zip(columns, result))

    # Renvoyer le dictionnaire sous forme de JSON avec JsonResponse
    return JsonResponse(result_dict)



def mis_qte(request):
    if request.method == 'POST':
        # Récupérer les données JSON envoyées par le client
        try:
            data = json.loads(request.body)

            # Extraire les valeurs de l'objet JSON
            part_number = data.get('part_number')
            serial_number = data.get('serial_number')
            quantite = data.get('quantite')
            operation = data.get('operation')
            commentaire = data.get('commentaire')

            if (int(quantite) > 0):
                #with connection.cursor() as cursor:
                #    cursor.execute("{cALL [dbo].[PS_QTE] (""'"+ part_number +"'"",""'"+quantite+"'"",""'"+operation+"'"",""'"+commentaire+"'"")}")
                #    result = cursor.fetchone()  # ou cursor.fetchone() selon le cas
                
                with connection.cursor() as cursor:
                    # Appel de la procédure stockée avec des paramètres
                    cursor.execute(
                        "{cALL [dbo].[PS_QTE] (%s, %s, %s, %s)}",
                        [
                            serial_number,
                            quantite,
                            operation,
                            commentaire
                        ]
                    )                   
                    # Récupérer un enregistrement
                    result = cursor.fetchone()  # ou cursor.fetchall() selon le cas

                # Récupérer le retour de la procédure, par exemple, un message ou un code d'erreur
                if result:
                    code_retour = result[0]
                    if code_retour == '1':  # Enregistrement avec succès
                    
                    # Récupérer les données mises à jour pour le tableau
                        # Remplacez cette partie par votre logique pour récupérer les données de la base
                        updated_data = []  # Ceci devrait être votre nouvelle liste de données
                        # Par exemple, quelque chose comme :
                        # updated_data = list(Produit.objects.values())

                        # Retourner une réponse JSON indiquant le succès et les données mises à jour
                        return JsonResponse({'status': 'success', 'message': 'matériel ajouté avec succès!', 'data': updated_data})
                    elif code_retour == '0':
                        return JsonResponse({'status': 'error', 'message': 'Ce matériel ne dispose pas d''un stock suffisant.!'})
                    else:  # part_number existe déjà
                        return JsonResponse({'status': 'error', 'message': 'Erreur lors de l''insertion.'}, status=400)
            else:      
                return JsonResponse({'status': 'error', 'message': 'La quantité ne doit pas être <= à 0'}, status=400)
            
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'La quantité ne doit pas être négatif.'}, status=400)
    else :
        # Si ce n'est pas une requête POST
        return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée.'}, status=405)
    



def InsertionPrdt(request):
    if request.method == 'POST':
        # Récupérer les données JSON envoyées par le client
        try:
            data = json.loads(request.body)

            # Extraire les valeurs de l'objet JSON
            part_number = data.get('part_number')
            designation = data.get('designation')
            serial_number = data.get('serial_number')
            type_equipement = data.get('type_equipement')
            seuil_alerte = data.get('seuil_alerte')
            id_emplacement = data.get('id_emplacement')
            detail_emplacement = data.get('detail_emplacement')


            if(part_number and designation and serial_number and type_equipement and seuil_alerte and id_emplacement and detail_emplacement):

                if (int(seuil_alerte) > 0):
                    
                    #with connection.cursor() as cursor:
                    #    cursor.execute("{cALL [dbo].[PS_PRODUIT] (""'"+ part_number +"'"",""'"+designation+"'"",""'"+serial_number+"'"",""'"+type_equipement+"'"",""'"+str(id_emplacement)+"'"",""'"+str(seuil_alerte)+"'"",""'"+detail_emplacement+"'"",0)}")
                    #    result = cursor.fetchone()  # ou cursor.fetchone() selon le cas

                    with connection.cursor() as cursor:
                        # Utiliser des paramètres pour éviter les problèmes d'injection SQL et d'échappement
                        cursor.execute(
                            "{cALL [dbo].[PS_PRODUIT] (%s, %s, %s, %s, %s, %s, %s, 0)}",
                            [
                                part_number,
                                designation,
                                serial_number,
                                type_equipement,
                                str(id_emplacement),
                                str(seuil_alerte),
                                detail_emplacement,
                            ]
                        )
                        result = cursor.fetchone()  # ou cursor.fetchall() selon le cas

                    # Récupérer le retour de la procédure, par exemple, un message ou un code d'erreur
                    if result:
                        code_retour = result[0]
                        print(result[0])
                        if code_retour == serial_number: #part_number:  # Enregistrement avec succès
                        
                            # Récupérer les données mises à jour pour le tableau
                            # Remplacez cette partie par votre logique pour récupérer les données de la base
                            updated_data = []  # Ceci devrait être votre nouvelle liste de données
                            # Par exemple, quelque chose comme :
                            # updated_data = list(Produit.objects.values())

                            # Retourner une réponse JSON indiquant le succès et les données mises à jour
                            return JsonResponse({'status': 'success', 'message': 'Matériel créé avec succès!', 'data': updated_data})

                        else:  # part_number existe déjà
                            return JsonResponse({'status': 'error', 'message': 'Erreur lors de l''insertion.'}, status=400)
                else:      
                    return JsonResponse({'status': 'error', 'message': 'Le seuil doit être supérieur à 0'}, status=400)
            else:      
                    return JsonResponse({'status': 'error', 'message': 'Veuillez renseigner tous les champs'}, status=400)
            
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'La seuil doit être superieur à 0.'}, status=400)
    else :
        # Si ce n'est pas une requête POST
        return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée.'}, status=405)
    


def mouv_partnumber_data(request):

    if request.method == 'POST':

        # Extraire les valeurs de l'objet JSON
        data = json.loads(request.body)
        partnumber = data.get('partnumber')

        #with connection.cursor() as cursor:
            #cursor.execute("{CALL [dbo].[MOUV_PRODUIT] (?)}", [part_number])
        #    cursor.execute("{cALL [dbo].[MOUV_PRODUIT] (""'"+ part_number +"'"")}")       
        #    result = cursor.fetchall()

        with connection.cursor() as cursor:
            cursor.execute(
                "{CALL [dbo].[MOUV_PRODUIT_PARTNUMBER] (%s)}",
                [partnumber]
            )
            # Récupérer tous les enregistrements
            result = cursor.fetchall()

            if result:
                # Convertir le résultat en liste de dictionnaires
                columns = [col[0] for col in cursor.description]
                data_result = [dict(zip(columns, row)) for row in result]
                #print(data_result)
                if data_result:
                    return JsonResponse({
                        'status': 'success',
                        'message': 'Données récupérées avec succès!',
                        'donnees': data_result
                        })
                else:
                    return JsonResponse({'status': 'success', 'message': 'Aucune ligne!'})
           
    # Renvoyer le dictionnaire sous forme de JSON avec JsonResponse
    return JsonResponse({'status': 'success', 'message': 'Aucune ligne!'})