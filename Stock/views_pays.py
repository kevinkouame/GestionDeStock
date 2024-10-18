from django.shortcuts import render
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json


def pays(request):
    
    with connection.cursor() as cursor:
        cursor.execute("{cALL [dbo].[LISTE_PAYS]}")
        pays = cursor.fetchall()  # Récupère les résultats sous forme de liste de tuples
        print(pays)  # Imprime les données récupérées pour vérifier leur structure

    return render(request, 'stock/pays.html', {'List_Pays': pays})


def savepays(request): # Utiliser pour la creation et la modification

    if request.method == 'POST':
        try:
            # Charger les données JSON du corps de la requête
            data = json.loads(request.body)

            # Récupérer les données
            id = data.get('id').strip()
            pays = data.get('pays').strip()

            with connection.cursor() as cursor:
                cursor.execute(
                     "{cALL [dbo].[PS_PAYS] (%s, %s)}",
                        [
                            pays,
                            id,
                        ]
                    )
                result = cursor.fetchone()  # ou cursor.fetchall() selon le cas
            
                # Récupérer le retour de la procédure, par exemple, un message ou un code d'erreur
                if result:
                    code_retour = result[0]
                    if code_retour == 1:
                        
                        Message = "La création a été effectuée avec succès"
                        if(id != ""):
                            Message = "La modification a été effectuée avec succès"

                        return JsonResponse({'status': 'success', 'message': Message})
                    else :
                        return JsonResponse({'status': 'success', 'message': 'Ce pays est déjà enregistré'})
                
        except Exception as e :
            print(str(e))
            return JsonResponse({'status': 'error', 'message': 'Une erreur est survenue'})
        
    else:
        return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée'}, status=405)



def deletepays(request): # Utiliser pour la creation et la modification

    if request.method == 'POST':
        try:
            # Charger les données JSON du corps de la requête
            data = json.loads(request.body)

            # Récupérer les données
            id = data.get('id').strip()
            
            with connection.cursor() as cursor:
                cursor.execute(
                     "{cALL [dbo].[DELETE_PAYS] (%s)}",
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








