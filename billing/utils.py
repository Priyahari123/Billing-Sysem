from .models import Denomination
from io import BytesIO
from django.template.loader import get_template
from xhtml2pdf import pisa

def calculate_balance_denominations(balance):
    """
    Calculates denomination breakup for the given balance amount
    using available shop denominations (greedy approach).
    """
    result = []
    denoms = Denomination.objects.order_by('-value')

    for d in denoms:
        count = int(balance // d.value)
        if count > 0:
            result.append({
                "value": d.value,
                "count": count
            })
            balance -= d.value * count

    return result




def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html = template.render(context_dict)

    result = BytesIO()
    pdf = pisa.CreatePDF(
        src=html,
        dest=result
    )

    if pdf.err:
        return None

    return result.getvalue()