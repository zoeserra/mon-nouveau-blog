from django.shortcuts import render
from django.utils import timezone
from .models import Character, Equipement

from django.shortcuts import get_object_or_404, redirect
from .forms import MoveForm




def post_list(request):
    characters = Character.objects.all().order_by('id_character')
    equipements = Equipement.objects.all()
    return render(request, 'blog/post_list.html', {'characters': characters, 'equipements': equipements})


from django.shortcuts import render, get_object_or_404

def post_detail(request, pk):
    character = get_object_or_404(Character, pk=pk)
    return render(request, 'blog/post_detail.html', {'character': character})

 
def character_list(request):
    characters = Character.objects.filter()
    return render(request, 'blog/character_list.html', {'characters': characters})
 
def character_detail(request, id_character):
    character = get_object_or_404(Character, id_character=id_character)
    message = ''  # Initialisation d'un message vide

    # Récupérer l'ancien lieu AVANT d'appliquer les modifications du formulaire
    ancien_lieu = get_object_or_404(Equipement, id_equip=character.lieu.id_equip)
    print(f"Ancien lieu: {ancien_lieu.id_equip}, disponibilité avant: {ancien_lieu.disponibilite}")

    if request.method == 'POST':
        form = MoveForm(request.POST, instance=character)

        if form.is_valid():
            # Récupérer les modifications du formulaire, mais sans les enregistrer dans la base de données
            character = form.save(commit=False)

            # Récupérer le nouveau lieu où le personnage sera déplacé
            nouveau_lieu = get_object_or_404(Equipement, id_equip=character.lieu.id_equip)
            print(f"Nouveau lieu avant mise à jour: {nouveau_lieu.id_equip}, disponibilité avant: {nouveau_lieu.disponibilite}")

            # Vérification si le nouveau lieu est libre, sauf pour la litière
            if nouveau_lieu.disponibilite != 'libre' and (nouveau_lieu.id_equip == 'salle de bain' or nouveau_lieu.id_equip == "salle de sport"):
                form.add_error('lieu', f'Le lieu {nouveau_lieu.id_equip} est actuellement occupé.')
                message = f'Le lieu {nouveau_lieu.id_equip} est actuellement occupé. Impossible de déplacer le personnage.'
            else:
                # 1. Marquer l'ancien lieu comme libre avant de sauvegarder le personnage
                ancien_lieu.disponibilite = 'libre'
                ancien_lieu.save()

                # Recharger l'objet après modification pour s'assurer que la mise à jour a été prise en compte
                ancien_lieu.refresh_from_db()
                print(f"Ancien lieu après mise à jour: {ancien_lieu.id_equip}, disponibilité après: {ancien_lieu.disponibilite}")

                # 2. Sauvegarder le personnage avec son nouveau lieu
                character.save()

                # 3. Marquer le nouveau lieu comme occupé (si ce n'est pas la litière)
                if nouveau_lieu.id_equip == 'salle de bain' or nouveau_lieu.id_equip == "salle de sport":  # La litière n'a pas besoin d'être occupée
                    nouveau_lieu.disponibilite = 'occupé'
                nouveau_lieu.save()

                # Recharger le nouveau lieu pour s'assurer que l'occupation a bien été prise en compte
                nouveau_lieu.refresh_from_db()
                print(f"Nouveau lieu après mise à jour: {nouveau_lieu.id_equip}, disponibilité après: {nouveau_lieu.disponibilite}")

                # 4. Mise à jour de l'état du personnage en fonction de son nouveau lieu
                if character.lieu.id_equip == 'cuisine' and character.etat == 'affamée':
                    character.etat = 'repus'
                elif character.lieu.id_equip == "salle de sport" and character.etat == 'repus':
                    character.etat = 'sale'
                elif character.lieu.id_equip == 'chambre' and character.etat == 'fatiguée':
                    character.etat = 'endormie'
                elif character.lieu.id_equip == 'salon' and character.etat == 'endormie':
                    character.etat = 'affamée'
                elif character.lieu.id_equip == 'salle de bain' and character.etat == 'sale':
                    character.etat = 'fatiguée'

                # Sauvegarder l'état du personnage après changement
                character.save()

                # Retourner à la page de détails du personnage après mise à jour
                return redirect('character_detail', id_character=character.id_character)

    else:
        form = MoveForm(instance=character)

    return render(request, 'blog/character_detail.html', {
        'character': character,
        'form': form,
        'message': message
    })
