"""Taxonomie commune : 14 familles, 85 intentions.

Les 77 intentions de Banking77 gardent leur nom d'origine, en anglais : le
classifieur est entraîné sur Banking77 tel quel, sans traduction (l'encodeur
est multilingue). Les 8 intentions créées par l'équipe sont en français.

La première intention de chaque famille sert de représentante quand seule la
famille est connue (par exemple après une escalade).
"""

from __future__ import annotations

INCONNUE = "inconnue"

FAMILLES: dict[str, tuple[str, ...]] = {
    # ── Familles Banking77 (77 intentions) ──
    "carte_perdue": (
        "lost_or_stolen_card", "compromised_card", "card_swallowed", "lost_or_stolen_phone",
    ),
    "carte_usage": (
        "card_not_working", "contactless_not_working", "pin_blocked", "change_pin",
        "activate_my_card", "card_about_to_expire", "card_acceptance",
        "declined_card_payment", "virtual_card_not_working", "pending_card_payment",
    ),
    "carte_commande": (
        "order_physical_card", "card_arrival", "card_delivery_estimate", "get_physical_card",
        "getting_spare_card", "getting_virtual_card", "get_disposable_virtual_card",
        "disposable_card_limits", "card_linking", "visa_or_mastercard",
        "supported_cards_and_currencies", "apple_pay_or_google_pay",
    ),
    "frais_contestation": (
        "extra_charge_on_statement", "card_payment_fee_charged", "transfer_fee_charged",
        "cash_withdrawal_charge", "exchange_charge", "top_up_by_card_charge",
        "top_up_by_bank_transfer_charge", "transaction_charged_twice",
        "card_payment_not_recognised", "direct_debit_payment_not_recognised",
        "cash_withdrawal_not_recognised", "request_refund", "Refund_not_showing_up",
        "reverted_card_payment?",
    ),
    "virement": (
        "faire_virement",  # nouvelle intention, représentante de la famille
        "transfer_into_account", "cancel_transfer", "pending_transfer", "transfer_timing",
        "failed_transfer", "declined_transfer", "beneficiary_not_allowed",
        "transfer_not_received_by_recipient", "receiving_money",
        "balance_not_updated_after_bank_transfer",
    ),
    "compte_identite": (
        "edit_personal_details", "verify_my_identity", "why_verify_identity",
        "unable_to_verify_identity", "verify_source_of_funds", "passcode_forgotten",
        "terminate_account", "age_limit",
    ),
    "especes": (
        "atm_support", "pending_cash_withdrawal", "declined_cash_withdrawal",
        "wrong_amount_of_cash_received", "balance_not_updated_after_cheque_or_cash_deposit",
    ),
    "change_etranger": (
        "exchange_rate", "card_payment_wrong_exchange_rate",
        "wrong_exchange_rate_for_cash_withdrawal", "exchange_via_app",
        "fiat_currency_support", "country_support",
    ),
    "alimenter_compte": (
        "automatic_top_up", "pending_top_up", "top_up_limits", "top_up_reverted",
        "topping_up_by_card", "top_up_failed", "verify_top_up", "top_up_by_cash_or_cheque",
    ),
    # ── Familles créées par l'équipe ──
    "epargne": ("epargne_projet",),
    "credit": ("credit_immobilier", "credit_conso", "pret_etudiant"),
    "aide": ("question_definition",),
    "insatisfaction": ("insatisfaction",),
    "conversation": ("hors_sujet",),
}

NOUVELLES_INTENTIONS: tuple[str, ...] = (
    "epargne_projet", "credit_immobilier", "credit_conso", "pret_etudiant",
    "faire_virement", "question_definition", "insatisfaction", "hors_sujet",
)

INTENTION_VERS_FAMILLE: dict[str, str] = {
    intention: famille for famille, intentions in FAMILLES.items() for intention in intentions
}

INTENTIONS_BANKING77: tuple[str, ...] = tuple(
    i for i in INTENTION_VERS_FAMILLE if i not in NOUVELLES_INTENTIONS
)

LIBELLES_FAMILLES: dict[str, str] = {
    "carte_perdue": "une carte perdue ou volée",
    "carte_usage": "l'utilisation de votre carte",
    "carte_commande": "la commande d'une carte",
    "frais_contestation": "des frais ou une opération contestée",
    "virement": "un virement",
    "compte_identite": "votre compte ou votre identité",
    "especes": "un retrait ou un dépôt d'espèces",
    "change_etranger": "le change ou l'étranger",
    "alimenter_compte": "l'alimentation de votre compte",
    "epargne": "votre épargne",
    "credit": "un crédit",
    "aide": "une explication",
    "insatisfaction": "une réclamation",
    "conversation": "autre chose",
}


def famille_de(intention: str) -> str:
    """Famille d'une intention, ou ``INCONNUE``."""

    return INTENTION_VERS_FAMILLE.get(intention, INCONNUE)


def representante(famille: str) -> str:
    """Intention représentante d'une famille, ou ``INCONNUE``."""

    intentions = FAMILLES.get(famille)
    return intentions[0] if intentions else INCONNUE
