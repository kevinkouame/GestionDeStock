from django.shortcuts import render
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json


def ListEmplacement(request):
    

    with connection.cursor() as cursor:
        cursor.execute("{cALL [dbo].[LISTE_PAYS]}")
        ListePays = cursor.fetchall()  # Récupère les résultats sous forme de liste de tuples
        print(ListePays)  # Imprime les données récupérées pour vérifier leur structure


    with connection.cursor() as cursor:
        cursor.execute("{cALL [dbo].[LISTE_EMPLACEMENT]}")
        ListeEmplacement = cursor.fetchall()  # Récupère les résultats sous forme de liste de tuples
        print(ListeEmplacement)  # Imprime les données récupérées pour vérifier leur structure

    return render(request, 'stock/emplacement.html', {'List_Emplacement': ListeEmplacement, 'List_Pays': ListePays })


def saveemplacement(request): # Utiliser pour la creation et la modification

    if request.method == 'POST':
        try:
            # Charger les données JSON du corps de la requête
            data = json.loads(request.body)

            # Récupérer les données
            id = data.get('id').strip()
            emplacement = data.get('emplacement').strip()
            pays = data.get('pays').strip()

            with connection.cursor() as cursor:
                cursor.execute(
                     "{cALL [dbo].[PS_EMPLACEMENT] (%s, %s, %s)}",
                        [
                            emplacement,
                            pays,
                            id,
                        ]
                    )
                result = cursor.fetchone()  # ou cursor.fetchall() selon le cas
            
                # Récupérer le retour de la procédure, par exemple, un message ou un code d'erreur
                if result:
                    code_retour = result[0]
                    if code_retour :
                        
                        Message = "La création a été effectuée avec succès"
                        if(id != ""):
                            Message = "La modification a été effectuée avec succès"

                        return JsonResponse({'status': 'success', 'message': Message})
                    else :
                        return JsonResponse({'status': 'success', 'message': 'Échec de la création'})
                
        except Exception as e :
            print(str(e))
            return JsonResponse({'status': 'error', 'message': 'Une erreur est survenue'})
        
    else:
        return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée'}, status=405)



def deleteEmplacement(request): # Utiliser pour la creation et la modification

    if request.method == 'POST':
        try:
            # Charger les données JSON du corps de la requête
            data = json.loads(request.body)

            # Récupérer les données
            id = data.get('id').strip()
            
            with connection.cursor() as cursor:
                cursor.execute(
                     "{cALL [dbo].[DELETE_EMPLACEMENT] (%s)}",
                        [
                            int(id),
                        ]
                    )
                result = cursor.fetchone()  # ou cursor.fetchall() selon le cas
            
                # Récupérer le retour de la procédure, par exemple, un message ou un code d'erreur
                if result:
                    code_retour = result[0]
                    if code_retour == 1:
                        Message = 'La suppression a été effectuée avec succès'

                        return JsonResponse({'status': 'success', 'message': Message})
                    else :
                        return JsonResponse({'status': 'success', 'message': 'Échec de la suppression'})
                
        except Exception as e :
            print(str(e))
            return JsonResponse({'status': 'error', 'message': 'Une erreur est survenue'})
        
    else:
        return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée'}, status=405)

