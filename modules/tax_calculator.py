import streamlit as st
from typing import Tuple
from modules.tax_constants import TaxConstants

class EstateTaxCalculator:
    """遺產稅計算器"""

    def __init__(self, constants: TaxConstants):
        self.constants = constants

    def compute_deductions(
        self,
        spouse: bool,
        adult_children: int,
        other_dependents: int,
        disabled_people: int,
        parents: int
    ) -> float:
        """計算扣除額總計"""
        spouse_deduction = self.constants.SPOUSE_DEDUCTION_VALUE if spouse else 0
        total_deductions = (
            spouse_deduction +
            self.constants.FUNERAL_EXPENSE +
            (disabled_people * self.constants.DISABLED_DEDUCTION) +
            (adult_children * self.constants.ADULT_CHILD_DEDUCTION) +
            (other_dependents * self.constants.OTHER_DEPENDENTS_DEDUCTION) +
            (parents * self.constants.PARENTS_DEDUCTION)
        )
        return total_deductions

    @st.cache_data
    def calculate_estate_tax(
        _self,
        total_assets: float,
        spouse: bool,
        adult_children: int,
        other_dependents: int,
        disabled_people: int,
        parents: int
    ) -> Tuple[float, float, float]:
        """計算課稅遺產淨額與稅額"""
        deductions = _self.compute_deductions(
            spouse, adult_children, other_dependents, disabled_people, parents
        )
        exempted_total = _self.constants.EXEMPT_AMOUNT + deductions

        if total_assets < exempted_total:
            return 0.0, 0.0, deductions

        taxable_amount = max(0, total_assets - exempted_total)
        tax_due = 0.0
        previous_bracket = 0

        for bracket, rate in _self.constants.TAX_BRACKETS:
            if taxable_amount > previous_bracket:
                taxable_at_rate = min(taxable_amount, bracket) - previous_bracket
                tax_due += taxable_at_rate * rate
                previous_bracket = bracket

        return taxable_amount, round(tax_due, 0), deductions
