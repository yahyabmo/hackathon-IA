"""Conseil bancaire explicable : stub initial pour le module de Sohayb."""

from ..contrats import Conseil


def conseiller(client_id: str, intention: str, slots: dict) -> Conseil:
    """Retourne un conseil vide tant que les règles métier ne sont pas livrées."""

    return Conseil(
        manque=[] if intention == "inconnue" else ["règles métier à définir"],
        alertes=[f"Conseil provisoire pour le client {client_id}"],
        faits={"intention": intention, "slots_reçus": slots},
    )
